import scrapy
from fp.fp import FreeProxy
from random_user_agent.params import OperatingSystem
from random_user_agent.user_agent import UserAgent

from AmazonWatcher.items import AmazonItem


class ItemscraperSpider(scrapy.Spider):
    name = 'itemscraper'
    allowed_domains = []

    def start_requests(self):
        user_agent_rotator = UserAgent(operating_systems=[OperatingSystem.LINUX.value,OperatingSystem.WINDOWS.value],limit=100)
        start_urls = [
                            'https://www.amazon.in/Blue-Tokai-Coffee-Roasters-Vienna/dp/B079684SRX/ref=sr_1_6'
                ]

        for url in start_urls:  
            proxy = FreeProxy(timeout=1,rand=True,anonym=True).get()
            yield scrapy.Request(url=url, callback=self.parse,
                                meta={"proxies":proxy},
                                headers={"User-Agent":user_agent_rotator.get_random_user_agent()}
                                )

    def parse(self, response):
        title = response.xpath('//*[@id="productTitle"]/text()').extract_first().strip()
        price = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first()

        if not price:
            price = response.xpath('//*[@id="priceblock_dealprice"]/text()').extract_first()
        price = "".join(i for i in price if i.isdigit() or i == ".").split(".")[0]
        
        item = AmazonItem(title,response.request.url,price,1)

        yield item