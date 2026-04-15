# art_call_aggregator/settings.py
BOT_NAME = 'art_call_aggregator'
SPIDER_MODULES = ['art_call_aggregator.spiders']
NEWSPIDER_MODULE = 'art_call_aggregator.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure a delay between requests to the same website
DOWNLOAD_DELAY = 2  # Seconds

# Set a realistic User-Agent
USER_AGENT = 'ArtCallAggregatorBot/1.0 (+https://github.com/yourusername/yourproject)'

# Pipelines to process items (e.g., save to database, filter duplicates)
# ITEM_PIPELINES = {
#    'art_call_aggregator.pipelines.DuplicatesPipeline': 300,
#    'art_call_aggregator.pipelines.SaveToDatabasePipeline': 400,
# }
