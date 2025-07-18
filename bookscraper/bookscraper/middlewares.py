# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from http.client import responses

from scrapy import signals
import requests
from urllib.parse import urlencode
from random import randint

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    async def process_start(self, start):
        # Called with an async iterator over the spider start() method or the
        # maching method of an earlier spider middleware.
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class BookscraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


import requests
from urllib.parse import urlencode
from random import randint

class ScrapeOpsFakeUserAgentMiddleware:
    def __init__(self, settings):
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get(
            'SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT',
            'https://headers.scrapeops.io/v1/user-agents'
        )
        self.scrapeops_fake_user_agents_active = settings.get('SCRAPOPS_FAKE_USER_AGENTS_ENABLED', True)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')
        self.user_agent_list = []

        self._get_user_agents_list()
        self._scrapeops_fake_user_agents_enabled()  # fixed method name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def _get_user_agents_list(self):
        payload = {'api_key': self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.user_agent_list = json_response.get('result', [])

    def _get_random_user_agent(self):
        if not self.user_agent_list:
            raise Exception("User agent list is empty. Check your ScrapeOps API key or network.")
        random_index = randint(0, len(self.user_agent_list) - 1)
        return self.user_agent_list[random_index]

    def _scrapeops_fake_user_agents_enabled(self):
        if not self.scrapeops_api_key or not self.scrapeops_endpoint:
            self.scrapeops_fake_user_agents_active = False
        else:
            self.scrapeops_fake_user_agents_active = True

    def process_request(self, request, spider):
        if self.scrapeops_fake_user_agents_active:
            request.headers['User-Agent'] = self._get_random_user_agent()

        print("********** NEW HEADER ATTACHED **********")
        print(request.headers['User-Agent'])




class ScrapeOpsFakeBrowserHeaderAgentMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get(
            'SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT',
            'https://headers.scrapeops.io/v1/browser-headers'
        )
        self.scrapeops_fake_browser_headers_active = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED', True)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')
        self.headers_list = []

        self._get_headers_list()
        self._scrapeops_fake_browser_header_enabled()

    def _get_headers_list(self):
        payload = {'api_key': self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        try:
            response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
            response.raise_for_status()
            json_response = response.json()
            self.headers_list = json_response.get('result', [])
        except Exception as e:
            print(f"Failed to fetch browser headers: {e}")
            self.headers_list = []

    def _get_random_browser_header(self):
        if not self.headers_list:
            raise Exception("Browser headers list is empty. Check your ScrapeOps API key or network.")
        random_index = randint(0, len(self.headers_list) - 1)
        return self.headers_list[random_index]

    def _scrapeops_fake_browser_header_enabled(self):
        if not self.scrapeops_api_key or not self.scrapeops_endpoint:
            self.scrapeops_fake_browser_headers_active = False
        else:
            self.scrapeops_fake_browser_headers_active = True

    def process_request(self, request, spider):
        if self.scrapeops_fake_browser_headers_active:
            random_browser_header = self._get_random_browser_header()
            for key, value in random_browser_header.items():
                request.headers[key.title()] = value

        print("********** NEW HEADER ATTACHED **********")
        print(request.headers)