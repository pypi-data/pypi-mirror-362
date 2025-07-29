# niquests_negotiate_sspi/niquests_negotiate_sspi.pyi


import logging
from typing import Any

import niquests
from niquests import Response
from niquests.auth import AuthBase

_logger: logging.Logger


class HttpNegotiateAuth(AuthBase):
    _auth_info: tuple[str, str | None, str] | None
    _service: str
    _host: str | None
    _delegate: bool

    def __init__(
        self,
        username: str | None = ...,
        password: str | None = ...,
        domain: str | None = ...,
        service: str | None = ...,
        host: str | None = ...,
        *,
        delegate: bool = ...,
    ) -> None: ...

    def _retry_using_http_negotiate_auth(
        self, response: Response, scheme: str, args: dict[str, Any],
    ) -> Response: ...

    def _response_hook(self, r: Response, **kwargs) -> Response | None: ...

    def __call__(self, r: niquests.PreparedRequest) -> niquests.PreparedRequest: ...
