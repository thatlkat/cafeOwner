 # cafeOwner/scraper/spiders/pipelines.py
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from urllib.parse import urlparse
import re

DOMAIN_BLACKLIST = {
    "exhibizone.com",
}

class FilterPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        source_url = adapter.get('source_url')

        # Domain Blacklist Filter
        if source_url:
            try:
                domain = urlparse(source_url).netloc
                if any(blacklisted in domain for blacklisted in DOMAIN_BLACKLIST):
                    raise DropItem(f"Domain blacklisted: {source_url}")
            except Exception:
                raise DropItem(f"Malformed source URL: {source_url}")

        description = adapter.get('full_description', '').lower()
        title = adapter.get('title', '').lower()
        combined_text = title + " " + description

        # Online-Only Filter
        online_keywords = [
            "online only", "virtual gallery", "digital exhibition",
            "website exhibition", "no physical space"
        ]
        if any(keyword in combined_text for keyword in online_keywords):
             adapter['is_online_only'] = True # Mark it
             raise DropItem(f"Skipping online-only exhibit: {adapter.get('title')}")
        else:
             adapter['is_online_only'] = False

        # Vanity / Pay-to-Play Filter (Heuristic based)
        vanity_keywords = [
            "guaranteed exhibition", "all artists will be featured",
            "pay to show", "participation fee required for all"
        ]
        if any(keyword in combined_text for keyword in vanity_keywords):
            raise DropItem(f"Likely vanity/pay-to-play: {adapter.get('title')}")

        # High Fee Check (Example)
        fee_text = adapter.get('application_fee', '')
        if fee_text:
            fee_matches = re.findall(r'\$(\d+(\.\d{2})?)', fee_text)
            for match in fee_matches:
                try:
                    if float(match[0]) > 80.00: # Example threshold
                         # More nuanced check might be needed, this is basic
                        if "juried" not in combined_text and "award" not in combined_text:
                            raise DropItem(f"Potentially high fee without clear jurying: {adapter.get('title')} - {fee_text}")
                except ValueError:
                    pass

        return item

class DuplicatesPipeline:
     def __init__(self):
          self.urls_seen = set()

     def process_item(self, item, spider):
          adapter = ItemAdapter(item)
          url = adapter.get('description_url')
          if url in self.urls_seen:
               raise DropItem(f"Duplicate item found: {url}")
          else:
               self.urls_seen.add(url)
               return item
