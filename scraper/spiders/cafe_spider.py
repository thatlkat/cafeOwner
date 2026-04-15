# cafeOwner/scraper/spiders/cafe_spider.py
import scrapy
from art_call_scraper.items import ArtCallItem

class CafeSpider(scrapy.Spider):
    name = 'cafe'
    allowed_domains = ['callforentry.org']
    start_urls = ['https://artist.callforentry.org/festivals.php']

    def parse(self, response):
        # Example: Find links to individual call pages
        # NOTE: Update selectors based on actual site structure
        call_links = response.css('div.list-item a.call-link::attr(href)').getall()
        for link in call_links:
            yield response.follow(link, self.parse_call_page)

        # Example: Pagination
        # next_page = response.css('a.next-page::attr(href)').get()
        # if next_page:
        #     yield response.follow(next_page, self.parse)

    def parse_call_page(self, response):
        item = ArtCallItem()
        item['source_url'] = response.url
        item['description_url'] = response.url

        # NOTE: These selectors are placeholders! Inspect the site.
        item['title'] = response.css('h1.call-title::text').get()
        item['organization'] = response.css('div.org-name::text').get()
        item['deadline'] = response.css('span.deadline-date::text').get()
        # ... extract other fields using appropriate CSS or XPath selectors

        item['full_description'] = " ".join(response.css('div.call-description ::text').getall())
        item['application_fee'] = response.css('span.fee-amount::text').get()

        # Extract location, eligibility, etc.

        yield item
