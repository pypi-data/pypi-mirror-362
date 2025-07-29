# typings/niquests/adapters.pyi

from typing import Callable, Mapping, TypeVar

from niquests import PreparedRequest, Response
from urllib3_future import HTTPConnectionPool, HTTPSConnectionPool, ProxyManager, Retry

T = TypeVar("T", bound=HTTPAdapter)

class HTTPAdapter:
    def __init__(
        self,
        connections: int = ...,
        maxsize: int = ...,
        block: bool = ...,
        max_retries: int | Retry | None = ...,
        pool_kwargs: Mapping[str, object] = ...,
    ) -> None: ...

    def init_poolmanager(
        self,
        connections: int,
        maxsize: int,
        block: bool = ...,
        **pool_kwargs: object,
    ) -> None: ...

    def proxy_manager_for(
        self,
        proxy: str,
        **proxy_kwargs: object,
    ) -> ProxyManager: ...

    def cert_verify(
        self,
        conn: HTTPSConnectionPool,
        url: str,
        verify: bool | str | bytes,
        cert: str | bytes,
    ) -> None: ...

    def build_response(
        self,
        req: PreparedRequest,
        resp: object,
    ) -> Response: ...

    def get_connection(
        self,
        url: str,
        proxies: Mapping[str, str] | None = ...,
    ) -> HTTPConnectionPool | HTTPSConnectionPool: ...

    def request_url(
        self,
        request: PreparedRequest,
        proxies: Mapping[str, str] | None,
    ) -> str: ...

    def add_headers(
        self,
        request: PreparedRequest,
        **headers: str | float | bool,
    ) -> None: ...

    def proxy_headers(self, proxy: str) -> Mapping[str, str]: ...

    def send(
        self,
        request: PreparedRequest,
        stream: bool = ...,
        timeout: float | TimeoutSauce | None = ...,
        verify: bool | str | bytes = ...,
        cert: str | bytes = ...,
        proxies: Mapping[str, str] | None = ...,
        on_post_connection: Callable[[object], None] | None = ...,
        on_upload_body: Callable[[int, int | None, bool, bool], None] | None = ...,
        on_early_response: Callable[[Response], None] | None = ...,
        multiplexed: bool = ...,
    ) -> Response: ...
