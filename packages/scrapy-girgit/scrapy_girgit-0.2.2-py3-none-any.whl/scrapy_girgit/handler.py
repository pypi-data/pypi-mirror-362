import time
from typing import Type, TypeVar

from curl_cffi.requests import AsyncSession
from scrapy.core.downloader.handlers.http11 import (
    HTTP11DownloadHandler as HTTPDownloadHandler,
)
from scrapy.crawler import Crawler
from scrapy.http.headers import Headers
from scrapy.http.request import Request
from scrapy.http.response import Response
from scrapy.responsetypes import responsetypes
from scrapy.spiders import Spider
from scrapy.utils.defer import deferred_f_from_coro_f
from scrapy.utils.reactor import verify_installed_reactor
from twisted.internet.defer import Deferred

from scrapy_girgit.parser import CurlOptionsParser, RequestParser

ImpersonateHandler = TypeVar("ImpersonateHandler", bound="ImpersonateDownloadHandler")


class ImpersonateDownloadHandler(HTTPDownloadHandler):
    def __init__(self, crawler) -> None:
        settings = crawler.settings
        super().__init__(settings=settings, crawler=crawler)

        verify_installed_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")

    @classmethod
    def from_crawler(cls: Type[ImpersonateHandler], crawler: Crawler) -> ImpersonateHandler:
        return cls(crawler)
        
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

        async with AsyncSession(max_clients=1, curl_options=curl_options, curl_infos=curl_infos) as client:
            request_args = RequestParser(_request).as_dict()
            # no need to handle redirects here, scrapy redirect middleware handles it
            # default scrapy handler also dont handle redirect 
            # it just return the raw response
            request_args['allow_redirects'] = False 
            start_time = time.time()
            response = await client.request(**request_args)
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
