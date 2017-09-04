import scrapy
class DmozSpider(scrapy.Spider):
    name = 'dmoz'
    allowed_domains = ["www.mzitu.com"]
    start_urls = [
        "http://www.mzitu.com"
    ]
    rules = [
        Rule(SgmlLinkExtractor(allow=(r'http://www.mzitu.com/[a-z0-9]+?'))),
        Rule(SgmlLinkExtractor(allow=(r'http://www.mzitu.com/[a-z0-9]+?')), callback="parse_item"),
    ]
    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            # title = sel.xpath('a/text()').extract()
            link = sel.xpath('a/@href').extract()
            desc = sel.xpath('text()').extract()
            print( link )