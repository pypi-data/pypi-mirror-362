from __future__ import annotations

import base64
import hashlib
import logging
import socket
import struct
from urllib.parse import urlparse

import niquests
import pywintypes
import sspi
import sspicon
import win32security
from niquests.auth import AuthBase
from niquests.exceptions import HTTPError

_logger = logging.getLogger(__name__)


class HttpNegotiateAuth(AuthBase):
    _auth_info = None
    _service = "HTTP"
    _host = None
    _delegate = False

    def __init__(self, username: str | None = None, password: str | None = None, domain: str | None = None, service: str | None = None, host: str | None = None, *, delegate: bool = False):
        """Create a new Negotiate auth handler.

        Args:
         username: Username.
         password: Password.
         domain: NT Domain name. (Optional)
         service: Kerberos Service type for remote Service Principal Name.
             Default: 'HTTP'
         host: Host name for Service Principal Name.
             Default: Extracted from request URI
         delegate: Indicates that the user's credentials are to be delegated to the server.
             Default: False

         If username and password are not specified, the user's default credentials are used.
         This allows for single-sign-on to domain resources if the user is currently logged on
         with a domain account.

        """

        if username is not None and password is not None:
            self._auth_info = (username, domain, password)

        if service is not None:
            self._service = service

        if host is not None:
            self._host = host

        self._delegate = delegate

    def _retry_using_http_negotiate_auth(self, response: niquests.Response, scheme, args):
        # Check for existing auth header
        if "Authorization" in response.request.headers:
            return response

        # Determine target host
        if self._host is None:
            target_url = urlparse(response.request.url)
            self._host = target_url.hostname
            try:
                self._host = socket.getaddrinfo(self._host, None, 0, 0, 0, socket.AI_CANONNAME)[0][3]
            except socket.gaierror as e:
                _logger.info("Skipping canonicalization of name %s due to error: %s", self._host, e)

        target_spn = f"{self._service}/{self._host}"

        # Request mutual auth by default
        sc_flags = sspicon.ISC_REQ_MUTUAL_AUTH

        if self._delegate:
            sc_flags |= sspicon.ISC_REQ_DELEGATE

        # Set up SSPI connection structure
        pkg_info = win32security.QuerySecurityPackageInfo(scheme)
        client_auth = sspi.ClientAuth(scheme, targetspn=target_spn, auth_info=self._auth_info,
                                      scflags=sc_flags, datarep=sspicon.SECURITY_NETWORK_DREP)
        sec_buffer = win32security.PySecBufferDescType()

        # Channel Binding Hash (aka Extended Protection for Authentication)
        # If this is an SSL connection, we need to hash the peer certificate, prepend the RFC5929 channel binding type,
        # and stuff it into an SEC_CHANNEL_BINDINGS structure.
        # This should be sent along in the initial handshake or Kerberos auth will fail.
        if hasattr(response, "peercert") and response.peercert is not None:
            md = hashlib.sha256()
            md.update(response.peercert)
            appdata = "tls-server-end-point:".encode("ASCII")+md.digest()
            cbt_buf = win32security.PySecBufferType(pkg_info["MaxToken"], sspicon.SECBUFFER_CHANNEL_BINDINGS)
            cbt_buf.Buffer = struct.pack(f"LLLLLLLL{len(appdata)}s", 0, 0, 0, 0, 0, 0, len(appdata), 32, appdata)
            sec_buffer.append(cbt_buf)

        content_length = int(response.request.headers.get("Content-Length", "0"), base=10)

        if hasattr(response.request.body, "seek"):
            if content_length > 0:
                response.request.body.seek(-content_length, 1)
            else:
                response.request.body.seek(0, 0)

        # Consume content and release the original connection
        # to allow our new request to reuse the same one.
        response.raw.release_conn()
        request = response.request.copy()

        # this is important for some web applications that store
        # authentication-related info in cookies
        if response.headers.get("set-cookie"):
            request.headers["Cookie"] = response.headers.get("set-cookie")

        # Send initial challenge auth header
        try:
            error, auth = client_auth.authorize(sec_buffer)
            request.headers["Authorization"] = f"{scheme} {base64.b64encode(auth[0].Buffer).decode('ASCII')}"
            _logger.debug(f"Sending Initial Context Token - error={error} authenticated={client_auth.authenticated}")
        except pywintypes.error as e:
            _logger.debug(f"Error calling {e.funcname}: {e.strerror}", exc_info=e)
            return response

        # A streaming response breaks authentication.
        # This can be fixed by not streaming this request, which is safe
        # because the returned response3 will still have stream=True set if
        # specified in args. In addition, we expect this request to give us a
        # challenge and not the real content, so the content will be short
        # anyway.
        args_no_stream = dict(args, stream=False)
        response2 = response.connection.send(request, **args_no_stream)

        # Should get another 401 if we are doing challenge-response (NTLM)
        if response2.status_code != 401:
            # Kerberos may have succeeded; if so, finalize our auth context
            final = response2.headers.get("WWW-Authenticate")
            if final is not None:
                try:
                    # Sometimes Windows seems to forget to prepend 'Negotiate' to the success response,
                    # and we get just a bare chunk of base64 token. Not sure why.
                    final = final.replace(scheme, "", 1).lstrip()
                    token_buf = win32security.PySecBufferType(pkg_info["MaxToken"], sspicon.SECBUFFER_TOKEN)
                    token_buf.Buffer = base64.b64decode(final.encode("ASCII"))
                    sec_buffer.append(token_buf)
                    error, auth = client_auth.authorize(sec_buffer)
                    _logger.debug(f"Kerberos Authentication succeeded - error={error} authenticated={client_auth.authenticated}")
                except TypeError:
                    pass

            # Regardless of whether we finalized our auth context,
            # without a 401 we've got nothing to do. Update the history and return.
            response2.history.append(response)
            return response2

        # Consume content and release the original connection
        # to allow our new request to reuse the same one.
        response2.raw.release_conn()
        request = response2.request.copy()

        # Keep passing the cookies along
        if response2.headers.get("set-cookie"):
            request.headers["Cookie"] = response2.headers.get("set-cookie")

        # Extract challenge message from server
        challenge = [val[len(scheme)+1:] for val in response2.headers.get("WWW-Authenticate", "").split(", ") if scheme in val]
        if len(challenge) != 1:
            error = f"Did not get exactly one {scheme} challenge from server."
            raise HTTPError(error)

        # Add challenge to security buffer
        token_buf = win32security.PySecBufferType(pkg_info["MaxToken"], sspicon.SECBUFFER_TOKEN)
        token_buf.Buffer = base64.b64decode(challenge[0])
        sec_buffer.append(token_buf)
        _logger.debug("Got Challenge Token (NTLM)")

        # Perform next authorization step
        try:
            error, auth = client_auth.authorize(sec_buffer)
            request.headers["Authorization"] = "{} {}".format(scheme, base64.b64encode(auth[0].Buffer).decode("ASCII"))
            _logger.debug(f"Sending Response - error={error} authenticated={client_auth.authenticated}")
        except pywintypes.error as e:
            _logger.debug(f"Error calling {e[1]}: {e[2]}", exc_info=e)
            return response

        response3 = response2.connection.send(request, **args)

        # Update the history and return
        response3.history.append(response)
        response3.history.append(response2)

        return response3

    def _response_hook(self, r, **kwargs):
        if r.status_code == 401:
            for scheme in ("Negotiate", "NTLM"):
                if scheme.lower() in r.headers.get("WWW-Authenticate", "").lower():
                    return self._retry_using_http_negotiate_auth(r, scheme, kwargs)
        return None

    def __call__(self, r):
        r.headers["Connection"] = "Keep-Alive"
        r.register_hook("response", self._response_hook)
        return r
