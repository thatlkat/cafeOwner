# cafeOwner/scraper/spider/items.py
import scrapy

class ArtCallItem(scrapy.Item):
    title = scrapy.Field()
    organization = scrapy.Field()
    deadline = scrapy.Field()
    location_city = scrapy.Field()
    location_state = scrapy.Field()
    location_country = scrapy.Field()
    description_url = scrapy.Field()
    full_description = scrapy.Field()
    eligibility = scrapy.Field()
    application_fee = scrapy.Field()
    keywords = scrapy.Field()
    source_url = scrapy.Field()
    is_online_only = scrapy.Field()
    # Add any other fields you need
