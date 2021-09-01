import scraper_helper
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import urljoin
from scrapy.link import Link


class ScrapebaySpider(CrawlSpider):
    name = 'scrapebay'
    allowed_domains = ['scrapebay.com']
    start_urls = ['http://scrapebay.com/']

    rules = (
        Rule(LinkExtractor(),
             callback='parse_item',
             follow=True,
             process_links='absolute_url' #comment this for default behavior
             ),
    )

    def absolute_url(self, links: list[Link]) -> list[Link]:
        """[summary]Receives a list of Link objects and
            returns a list of Link objects with nocache appended.
        """
        updated_links = []
        for link in links:
            # Update the links
            link.url = urljoin(link.url, "?nocache")
            updated_links.append(link)
        return updated_links

    def parse_item(self, response):
        print(response.url)
        yield {
            'Title': response.css('title::text').get(),
            'Link': response.url,
        }


if __name__ == '__main__':
    scraper_helper.run_spider(ScrapebaySpider)
