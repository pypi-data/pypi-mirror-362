from collections import deque
import logging
import os
import time
from typing import List, Self, Dict, Any
from scrapy import logformatter
from scrapy.crawler import Crawler
from scrapy.exceptions import DropItem
from scrapy import Spider
from scrapy.http import Response
from scrapy.utils.python import global_object_name
from twisted.python.failure import Failure
from scrapy.logformatter import LogFormatterResult



class ZenLogFormatter(logformatter.LogFormatter):
    YELLOW = "\033[33m"
    RED = "\033[31m"
    RESET = "\033[0m"

    def __init__(self, truncate_fields: List[str]) -> None:
        self.truncate_fields = truncate_fields

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> Self:
        return cls(
            truncate_fields=crawler.settings.getlist("FORMATTER_TRUNCATE_FIELDS", []),
        )

    @staticmethod
    def truncate(value: Any, length=50) -> Any:
        if isinstance(value, str):
            return value[:length] + '...' if len(value) > length else value
        return value

    def dropped(self, item: Dict, exception: DropItem, response: Response, spider: Spider) -> LogFormatterResult:
        return {
            'level': logging.DEBUG,
            'msg': self.YELLOW + "Dropped: %(exception)s" + self.RESET + os.linesep + "%(item)s",
            'args': {
                'exception': exception,
                'item': {k:self.truncate(v) if k in self.truncate_fields else v for k,v in item.items()},
            }
        }

    def item_error(self, item: Dict, exception: DropItem, response: Response, spider: Spider) -> LogFormatterResult:
        return {
            'level': logging.ERROR,
            'msg': self.RED + "Error processing %(item)s" + self.RESET,
            'args': {
                'exception': exception,
                'item': {k:self.truncate(v) if k in self.truncate_fields else v for k,v in item.items()},
            }
        }

    def scraped(self, item: Dict, response: Response, spider: Spider) -> LogFormatterResult:
        src: Any
        if response is None:
            src = f"{global_object_name(spider.__class__)}.start_requests"
        elif isinstance(response, Failure):
            src = response.getErrorMessage()
        else:
            src = response
        return {
            "level": logging.DEBUG,
            "msg": "Scraped from %(src)s" + os.linesep + "%(item)s",
            "args": {
                "src": src,
                "item": {k:self.truncate(v) if k in self.truncate_fields else v for k,v in item.items()},
            },
        }
    

class ScrapyDictFormatter(logging.Formatter):

    def format(self, record):
        if isinstance(record.msg, dict):
            msg_dict = record.msg
            record.msg = msg_dict.get('format', str(msg_dict))
            record.args = msg_dict
        return super().format(record)



class ZenBufferedLogHandler(logging.Handler):

    def __init__(self, filename: str, length: int):
        super().__init__()
        self.filename = filename
        self.buffer = deque(maxlen=length)

    def emit(self, record):
        self.buffer.append(self.format(record))

    def flush(self):
        try:
            with open(self.filename, "a") as f:
                f.write("\n".join(self.buffer))
            self.buffer.clear()
        except Exception as e:
            logging.error(f"ZenBufferedLogHandler failed to flush to {self.filename}: {e}")

    