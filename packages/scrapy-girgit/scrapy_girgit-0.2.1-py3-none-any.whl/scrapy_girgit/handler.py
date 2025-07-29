from http.cookies import SimpleCookie
import time
from typing import Type, TypeVar

from curl_cffi.requests import AsyncSession
import scrapy
from scrapy.core.downloader.handlers.http11 import (
    HTTP11DownloadHandler as HTTPDownloadHandler,
)
from scrapy.crawler import Crawler
from scrapy.http.headers import Headers
from scrapy.http.request import Request
from scrapy.http.response import Response
from scrapy.responsetypes import responsetypes
import scrapy.signals
from scrapy.spiders import Spider
from scrapy.utils.defer import deferred_f_from_coro_f
from scrapy.utils.reactor import verify_installed_reactor
from twisted.internet.defer import Deferred

from scrapy_girgit.parser import CurlOptionsParser, RequestParser

ImpersonateHandler = TypeVar("ImpersonateHandler", bound="ImpersonateDownloadHandler")


class ImpersonateDownloadHandler(HTTPDownloadHandler):
    def __init__(self, crawler) -> None:
        self.settings = crawler.settings
        self.client: AsyncSession
        super().__init__(settings=self.settings, crawler=crawler)

        verify_installed_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")

    @classmethod
    def from_crawler(cls: Type[ImpersonateHandler], crawler: Crawler) -> ImpersonateHandler:
        h = cls(crawler)
        crawler.signals.connect(h.spider_opened, signal=scrapy.signals.spider_opened)
        crawler.signals.connect(h.spider_closed, signal=scrapy.signals.spider_closed)
        return h

    async def spider_opened(self, spider: Spider) -> None:
        curl_infos = self.settings.getlist("IMPERSONATE_CURL_INFOS", [])
        self.client = AsyncSession(max_clients=1, curl_infos=curl_infos)

    async def spider_closed(self, spider: Spider) -> None:
        if hasattr(self, "client") and self.client:
            await self.client.close()

    def download_request(self, request: Request, spider: Spider) -> Deferred:
        if request.meta.get("impersonate"):
            return self._download_request(request, spider)

        return super().download_request(request, spider)

    @deferred_f_from_coro_f
    async def _download_request(self, request: Request, spider: Spider) -> Response:
        # copy the request to avoid mutating the original in CurlOptionsParser (which pops headers)
        _request = request.copy()
        curl_options = CurlOptionsParser(_request).as_dict()
        # metrics that need to be calculated
        curl_infos = request.meta.get("impersonate_curl_infos", [])

        self.client.cookies.clear()
        if "Cookie" in request.headers:
            for name, morsel in SimpleCookie(request.headers.get("Cookie").decode("utf-8")).items():
                self.client.cookies.set(
                    name=name,
                    value=morsel.value,
                    domain=request.meta['download_slot']
                )
                
        request_args = RequestParser(_request).as_dict()
        # no need to handle redirects here, scrapy redirect middleware handles it
        # default scrapy handler also dont handle redirect 
        # it just return the raw response
        request_args['allow_redirects'] = False 
        start_time = time.time()
        response = await self.client.request(**request_args, curl_options=curl_options)
        download_latency = time.time() - start_time
        if curl_infos:
            request.meta['impersonate_curl_infos'] = response.infos

        headers = Headers(response.headers.multi_items())
        headers.pop("Content-Encoding", None)

        respcls = responsetypes.from_args(
            headers=headers,
            url=response.url,
            body=response.content,
        )

        resp = respcls(
            url=response.url,
            status=response.status_code,
            headers=headers,
            body=response.content,
            flags=["impersonate"],
            request=request,
        )
        resp.meta["download_latency"] = download_latency
        return resp
