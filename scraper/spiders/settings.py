# cafeOwner/scraper/spiders/settings.py
ITEM_PIPELINES = {
   'art_call_scraper.pipelines.DuplicatesPipeline': 100,
   'art_call_scraper.pipelines.FilterPipeline': 200,
   # Add other pipelines like saving to a file/DB, e.g.:
   # 'art_call_scraper.pipelines.JsonWriterPipeline': 300,
}

BOT_NAME = 'art_call_scraper'

SPIDER_MODULES = ['art_call_scraper.spiders']
NEWSPIDER_MODULE = 'art_call_scraper.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 8
# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 1  # 1 second delay
CONCURRENT_REQUESTS_PER_DOMAIN = 4

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Set a realistic User-Agent
USER_AGENT = 'ArtCallAggregator (+http://your-github-repo-url)'

# Other settings...
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
FEED_EXPORT_ENCODING = 'utf-8'
