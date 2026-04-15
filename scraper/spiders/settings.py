# cafeOwner/scraper/spiders/settings.py
ITEM_PIPELINES = {
   'art_call_scraper.pipelines.DuplicatesPipeline': 100,
   'art_call_scraper.pipelines.FilterPipeline': 200,
   # Add other pipelines like saving to a file/DB, e.g.:
   # 'art_call_scraper.pipelines.JsonWriterPipeline': 300,
}
