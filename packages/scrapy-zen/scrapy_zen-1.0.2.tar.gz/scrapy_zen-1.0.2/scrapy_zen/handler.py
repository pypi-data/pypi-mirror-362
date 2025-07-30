import random
from scrapy_playwright.handler import ScrapyPlaywrightDownloadHandler
from scrapy_zyte_api import ScrapyZyteAPIDownloadHandler
from scrapy_girgit import ImpersonateDownloadHandler
from scrapy.core.downloader.handlers.http import HTTPDownloadHandler
from twisted.internet.defer import Deferred
from scrapy.http import Request, Response
from scrapy import Spider
from scrapy.crawler import Crawler
from typing import Self
from scrapy import signals


impersonate_fingerprints = [
    "chrome99",
    "chrome99_android",
    "chrome100",
    "chrome101",
    "chrome104",
    "chrome107",
    "chrome110",
    "chrome116",
    "chrome119",
    "chrome120",
    "chrome123",
    "chrome124",
    "chrome131",
    "chrome131_android",
    "chrome133a",
    "edge99",
    "edge101",
    "safari15_3",
    "safari15_5",
    "firefox133",
    "firefox135",
]



class ZenDownloadHandler:
    lazy = False

    def __init__(self, crawler: Crawler):
        self.playwright_handler = ScrapyPlaywrightDownloadHandler.from_crawler(crawler)
        self.zyte_handler = ScrapyZyteAPIDownloadHandler.from_crawler(crawler)
        self.impersonate_handler = ImpersonateDownloadHandler.from_crawler(crawler)
        self.scrapy_default_handler = HTTPDownloadHandler.from_crawler(crawler)

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> Self:
        h = cls(crawler)
        crawler.signals.connect(h.spider_closed, signal=signals.spider_closed)
        return h

    def download_request(self, request: Request, spider: Spider) -> Deferred | Deferred[Response]:
        if request.meta.get('playwright'):
            return self.playwright_handler.download_request(request, spider)

        elif request.meta.get("impersonate"):
            impersonate = request.meta.get("impersonate")
            if impersonate == "random":
                request.meta["impersonate"] = random.choice(impersonate_fingerprints)
            return self.impersonate_handler.download_request(request, spider)

        elif request.meta.get('zyte_api_automap'):
            return self.zyte_handler.download_request(request, spider)
        else:
            return self.scrapy_default_handler.download_request(request, spider)

    async def spider_closed(self, spider: Spider) -> None:
        self.impersonate_handler.close()
        self.scrapy_default_handler.close()
        self.playwright_handler.close()
        self.zyte_handler.close()
