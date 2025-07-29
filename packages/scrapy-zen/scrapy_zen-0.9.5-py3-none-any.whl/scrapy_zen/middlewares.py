from collections import OrderedDict
import time
from zoneinfo import ZoneInfo
from scrapy import Spider
from scrapy.exceptions import IgnoreRequest
from datetime import datetime, timedelta, timezone
import dateparser
# from browserforge.headers import HeaderGenerator
from scrapy.http import Request, Response
from scrapy import signals


class PreProcessingMiddleware:
    """
    Downloader Middleware to preprocess requests before forwarding.
    Handles deduplication
    """

    # def __init__(self):
    #     self.header_generator = HeaderGenerator()


    def process_request(self, request: Request, spider: Spider) -> None:
        _dt = request.meta.pop("_dt", None)
        _dt_format = request.meta.pop("_dt_format", None)
        if _dt:
            if not self.is_recent(_dt, _dt_format, request.url, spider):
                raise IgnoreRequest
        # browserforge =  request.meta.pop("browserforge", None)
        # if browserforge:
        #     headers = self.header_generator.generate()
        #     request.headers.update(headers)
        request.meta['requested_at'] = int(time.time() * 1000)
        return None

    def process_response(self, request: Request, response: Response, spider: Spider) -> Response:
        if "impersonate" in request.meta: # bug in scrapy-impersonate
            response.request.meta['responded_at'] = int(time.time() * 1000)
        else:
            request.meta['responded_at'] = int(time.time() * 1000)
        return response

    def is_recent(self, date_str: str, date_format: str, debug_info: str, spider: Spider) -> bool:
        """
        Check if the date is recent (within the last 2 days).
        """
        try:
            if not date_str:
                return True
            utc_today = datetime.now(ZoneInfo('UTC')).date()
            input_date = dateparser.parse(date_string=date_str, date_formats=[date_format] if date_format is not None else None).date()
            return input_date >= (utc_today - timedelta(days=2))
        except Exception as e:
            spider.logger.error(f"{str(e)}: {debug_info} ")
            return False



class ZenSpiderMiddleware:

    async def process_spider_output(self, response, result, spider):
        async for i in result:
            if isinstance(i, dict):
                new_dict = OrderedDict()
                for k,v in i.items():
                    new_dict[k] = v
                    if k == "published_at":
                        new_dict['scraped_at'] = int(time.time() * 1000)
                new_dict['requested_at'] = response.meta.get("requested_at")
                new_dict['responded_at'] = response.meta.get("responded_at")
                yield new_dict
            else:
                yield i

    async def process_start(self, start):
        async for item_or_request in start:
            yield item_or_request
