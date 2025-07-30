import asyncio
import ssl
from collections import namedtuple
from contextlib import asynccontextmanager
from typing import Any, Callable, List, Mapping, Optional, Union
from urllib.parse import urljoin

from async_lru import alru_cache
from httpx import (
    USE_CLIENT_DEFAULT,
    AsyncBaseTransport,
    AsyncClient,
    ConnectError,
    Cookies,
    Limits,
    ProxyError,
    ReadTimeout,
    RemoteProtocolError,
    Response,
    Timeout,
    TimeoutException,
)
from httpx._client import UseClientDefault
from httpx._config import DEFAULT_LIMITS, DEFAULT_MAX_REDIRECTS
from httpx._types import (
    AuthTypes,
    CertTypes,
    CookieTypes,
    HeaderTypes,
    ProxiesTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestFiles,
    TimeoutTypes,
    URLTypes,
    VerifyTypes,
)
from protego import Protego
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from .metrics import register_scraper_client, request_timer

HTTP_RETRY_EXCEPTION_TYPES = (
    retry_if_exception_type(TimeoutException)
    | retry_if_exception_type(ConnectError)
    | retry_if_exception_type(ReadTimeout)
    | retry_if_exception_type(ProxyError)
    | retry_if_exception_type(RemoteProtocolError)
    | retry_if_exception_type(ssl.SSLZeroReturnError)
    | retry_if_exception_type(ssl.SSLError)
)

TimeoutTuple = namedtuple("TimeoutTuple", ["connect", "read", "write", "pool"])
DEFAULT_TIMEOUT = TimeoutTuple(30.0, 30.0, 30.0, 30.0)

# This default value is adjusted to match most of use cases.
MAKE_ROBOTS_TEXT_PARSER_CACHE_DECORATOR = alru_cache(maxsize=5)


@asynccontextmanager
async def without_restrictions():
    yield


class RobotFileParserTimeoutError(Exception):
    pass


class ScraperClient(AsyncClient):
    def __init__(
        self,
        *,
        auth: AuthTypes = None,
        params: QueryParamTypes = None,
        headers: HeaderTypes = None,
        cookies: CookieTypes = None,
        verify: VerifyTypes = True,
        cert: CertTypes = None,
        http1: bool = True,
        http2: bool = False,
        proxies: ProxiesTypes = None,
        mounts: Mapping[str, AsyncBaseTransport] = None,
        timeout: TimeoutTypes = DEFAULT_TIMEOUT,
        follow_redirects: bool = False,
        limits: Limits = DEFAULT_LIMITS,
        max_redirects: int = DEFAULT_MAX_REDIRECTS,
        event_hooks: Mapping[str, List[Callable]] = None,
        base_url: URLTypes = "",
        transport: AsyncBaseTransport = None,
        app: Callable = None,
        trust_env: bool = True,
        persist_cookies: bool = False,
        scraper_id: Union[str, None] = None,
        max_retry_attempts: int = 3,
        retry_wait_multiplier: int = 1,
        retry_wait_max: int = 1,
        ignore_robots_txt: bool = False,
        truncate_after: int = 1024000,  # 1 MB
        total_timeout: int = 180,  # 3 minutes
        make_robots_text_parser_cache_decorator: Optional[
            Callable
        ] = MAKE_ROBOTS_TEXT_PARSER_CACHE_DECORATOR,
        fetch_robots_text_cache_decorator: Optional[Callable] = None,
    ):
        super().__init__(
            auth=auth,
            params=params,
            headers=headers,
            cookies=cookies,
            verify=verify,
            cert=cert,
            http1=http1,
            http2=http2,
            proxies=proxies,
            mounts=mounts,
            timeout=timeout,
            follow_redirects=follow_redirects,
            limits=Limits(
                max_connections=limits.max_connections,
                max_keepalive_connections=limits.max_connections,
                keepalive_expiry=limits.keepalive_expiry,
            ),
            max_redirects=max_redirects,
            event_hooks=event_hooks,
            base_url=base_url,
            transport=transport,
            app=app,
            trust_env=trust_env,
        )
        self.scraper_id = scraper_id
        self.persist_cookies = persist_cookies
        self.ignore_robots_txt = ignore_robots_txt
        self.truncate_after = truncate_after
        self.total_timeout = total_timeout
        if limits.max_connections and limits.max_connections > 0:
            self.max_connections_semaphore = asyncio.Semaphore(limits.max_connections)
        else:
            self.max_connections_semaphore = None

        # Wrap request in retry decorator
        self.request = retry(
            stop=stop_after_attempt(max_retry_attempts),
            wait=wait_random_exponential(
                multiplier=retry_wait_multiplier, max=retry_wait_max
            ),
            retry=HTTP_RETRY_EXCEPTION_TYPES,
            reraise=True,
        )(self.request)

        if fetch_robots_text_cache_decorator:
            self.fetch_robots_txt = fetch_robots_text_cache_decorator(
                self.fetch_robots_txt
            )

        if make_robots_text_parser_cache_decorator:
            self.make_robots_txt_parser = make_robots_text_parser_cache_decorator(
                self.make_robots_txt_parser
            )

        register_scraper_client(self)

    async def request(
        self,
        method: str,
        url: URLTypes,
        *,
        content: RequestContent = None,
        data: RequestData = None,
        files: RequestFiles = None,
        json: Any = None,
        params: QueryParamTypes = None,
        headers: HeaderTypes = None,
        cookies: CookieTypes = None,
        auth: Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        follow_redirects: Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        extensions: dict = None,
        truncate_after: Optional[int] = None,
        ignore_robots_txt: Optional[bool] = None,
    ) -> Response:
        if ignore_robots_txt is None:
            ignore_robots_txt = self.ignore_robots_txt

        if truncate_after is None:
            truncate_after = self.truncate_after

        # we force the hashable timeout to enable cache
        if isinstance(timeout, Timeout):
            timeout = TimeoutTuple(
                timeout.connect, timeout.read, timeout.write, timeout.pool
            )

        async with self.max_connections_semaphore or without_restrictions():
            async with asyncio.timeout(self.total_timeout):
                return await self._request_truncated_content(
                    method,
                    url,
                    content=content,
                    data=data,
                    files=files,
                    json=json,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    auth=auth,
                    follow_redirects=follow_redirects,
                    timeout=timeout,
                    extensions=extensions,
                    truncate_after=truncate_after,
                    ignore_robots_txt=ignore_robots_txt,
                )

    async def _request_truncated_content(
        self,
        method: str,
        url: URLTypes,
        *,
        content: RequestContent = None,
        data: RequestData = None,
        files: RequestFiles = None,
        json: Any = None,
        params: QueryParamTypes = None,
        headers: HeaderTypes = None,
        cookies: CookieTypes = None,
        auth: Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        follow_redirects: Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        extensions: dict = None,
        truncate_after: Optional[int] = None,
        ignore_robots_txt: Optional[bool] = None,
    ):
        """
        Extends the httpx.AsyncClient.request()
        with truncate_after parameter
        """

        if not self.persist_cookies:
            self._cookies = Cookies(None)

        request = self.build_request(
            method=method,
            url=url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )
        if not ignore_robots_txt:
            user_agent = headers.get("user-agent", "*")
            if not await self.is_allowed_by_robots_text(
                url, user_agent, timeout=timeout
            ):
                return Response(
                    403,
                    text="403 Forbidden: Access to {url} is disallowed by the site's robots.txt file.",
                    request=request,
                )

        with request_timer(scraper_id=self.scraper_id):
            response = await self.send(
                request, auth=auth, follow_redirects=follow_redirects, stream=True
            )
            content: bytes = b""
            try:
                content_accumulator = bytearray()
                async for chunk in response.aiter_bytes():
                    content_accumulator.extend(chunk)
                    if truncate_after and len(content_accumulator) > truncate_after:
                        break
                response._content = bytes(content_accumulator[:truncate_after])
            finally:
                await response.aclose()

            return response

    async def fetch_robots_txt(
        self,
        base_url: str,
        user_agent: str,
        timeout: Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
    ) -> str:
        robots_txt_url = urljoin(base_url, "robots.txt")
        try:
            response = await self._request_truncated_content(
                "GET",
                robots_txt_url,
                headers={"user-agent": user_agent},
                follow_redirects=True,
                # The Robots Exclusion Protocol requires crawlers to parse at least 500 kibibytes (512000 bytes):
                truncate_after=512000,
                timeout=timeout or self.timeout,
                ignore_robots_txt=True,
            )
            if response.status_code == 200:
                robot_txt = response.text
            elif response.status_code in (401, 403):
                robot_txt = "User-agent: *\nDisallow: /"
            else:
                robot_txt = "User-agent: *\nAllow: /"
        except (TimeoutException, ReadTimeout):
            raise RobotFileParserTimeoutError(f"Timeout while loading {robots_txt_url}")
        return robot_txt

    async def make_robots_txt_parser(
        self,
        base_url,
        user_agent: str,
        timeout: Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
    ):
        robots_txt = await self.fetch_robots_txt(base_url, user_agent, timeout=timeout)
        return await asyncio.get_running_loop().run_in_executor(
            None, Protego.parse, robots_txt
        )

    async def is_allowed_by_robots_text(
        self,
        url: str,
        user_agent: str,
        timeout: Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
    ) -> bool:
        robots_text_parser = await self.make_robots_txt_parser(
            urljoin(url, "/"), user_agent, timeout=timeout
        )
        return robots_text_parser.can_fetch(url=url, user_agent=user_agent)
