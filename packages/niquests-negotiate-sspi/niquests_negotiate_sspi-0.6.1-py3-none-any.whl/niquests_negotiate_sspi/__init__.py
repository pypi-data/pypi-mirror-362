"""Allows for Single Sign-On (SSO) HTTP Negotiate authentication using the niquests library on Windows."""

import niquests

from .niquests_negotiate_sspi import HttpNegotiateAuth

__all__ = ["HttpNegotiateAuth"]

# Monkeypatch urllib3 to expose the peer certificate
http_adapter = niquests.adapters.HTTPAdapter
orig_http_adapter_build_response = http_adapter.build_response


def new_http_adapter_build_response(self, request, resp):
    response = orig_http_adapter_build_response(self, request, resp)
    try:
        response.peercert = resp._connection.sock.getpeercert(binary_form=True)  # noqa: SLF001
    except AttributeError:
        response.peercert = None
    return response


http_adapter.build_response = new_http_adapter_build_response
