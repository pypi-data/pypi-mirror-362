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

    def format(self, record):
        """
        Formats the log record.

        If the record's message is a dictionary (as is common with Scrapy's
        structured logging), it uses the 'format' key from that dictionary
        as the format string and the dictionary itself for the arguments.
        Otherwise, it falls back to the standard logging.Formatter behavior.
        """
        # Check if the core message is a dictionary
        if isinstance(record.msg, dict):
            # Scrapy's structured logs use a 'format' key for the template
            # and the dictionary itself for the values.
            # We use .get() to fall back gracefully if 'format' is missing.
            record.msg = record.msg.get('format', str(record.msg))
            record.args = record.args or record.msg

        # After potentially modifying the record, let the parent class
        # handle the actual string formatting (e.g., replacing %s, %d, etc.).
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
            with open(self.filename, "w") as f:
                f.write("\n".join(self.buffer))
            self.buffer.clear()
        except Exception as e:
            logging.error(f"ZenBufferedLogHandler failed to flush to {self.filename}: {e}")

    