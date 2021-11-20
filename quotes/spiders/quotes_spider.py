from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from ..items import QuotesItem


class QuotesSpider(Spider):
    name = "quotes-spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        """
        Scrape the required data from response object.
        In this case, it is quote, author of quote and
        tags associated with the quote.
        Also make new Request to the next web page, by
        extracting its URL from the current web page.
        :param response: response received
        :return: Item object.
        """
        for quote_selector in response.css("div.quote"):
            l = ItemLoader(item=QuotesItem(), selector=quote_selector)
            l.add_css("text", "span.text::text")
            l.add_css("author", "small.author::text")
            l.add_css("tags", "div.tags a.tag::text")
            yield l.load_item()

        next_page = response.css("li.next a::attr(href)").get()

        if next_page:
            next_page = response.urljoin(next_page)
            yield Request(next_page, self.parse)
