# art_call_aggregator/items.py
import scrapy

class ArtCallItem(scrapy.Item):
    title = scrapy.Field()
    organization = scrapy.Field()
    deadline = scrapy.Field()
    location = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    # Add other fields like application_fee, eligibility, etc.
    source_site = scrapy.Field() # To track where it came from
