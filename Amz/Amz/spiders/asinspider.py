from pytest import yield_fixture
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import AmzItem
from scrapy.loader import ItemLoader


class AsinspiderSpider(CrawlSpider):
    name = 'asinspider'
    allowed_domains = ['amazon.in']
    start_urls = ['http://amazon.in/s?k=monitor']

    rules = (
        Rule(LinkExtractor(allow='s?k=monitor&page=', restrict_css="a.s-pagination-next")),
        Rule(LinkExtractor(allow='/dp/'), callback='parse_item'),
    )

    def parse_item(self, response):
        l = ItemLoader(item=AmzItem(),response=response)
        l.add_css("name","span#productTitle")
        l.add_css("asin", "#ASIN::attr(value)")
        l.add_css("price","span.a-offscreen")
        l.add_css("discounted","span.savingsPercentage")
        l.add_css("totalreviews","span#acrCustomerReviewText")
        yield l.load_item()
