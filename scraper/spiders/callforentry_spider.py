import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse

# Assuming utils.py exists in the parent directory or is accessible
# from ..utils import is_likely_vanity_or_pay_to_play, is_internet_only, DOMAIN_BLACKLIST

class CallForEntrySpider:
    name = "callforentry"
    start_urls = ["https://www.callforentry.org/festivals.php"]
    base_url = "https://www.callforentry.org/"

    def __init__(self, max_pages=1):
        self.max_pages = max_pages
        self.visited_urls = set()

    def fetch_page(self, url):
        headers = {'User-Agent': 'ArtCallAggregator/1.0'}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse_listings(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        # ... Logic to find links to individual call detail pages ...
        # Example: (selector will depend on actual site structure)
        # call_links = soup.select("a.call-link")
        # for link in call_links:
        #     detail_url = urljoin(self.base_url, link['href'])
        #     yield detail_url
        pass # Placeholder

    def parse_detail_page(self, html_content, url):
        soup = BeautifulSoup(html_content, 'html.parser')

        # Placeholder for filter checks
        # if is_likely_vanity_or_pay_to_play(soup): return None
        # if is_internet_only(soup): return None

        item = {}
        # ... Logic to extract title, deadline, description, etc. ...
        # Example:
        # item['title'] = soup.select_one("h1.call-title").text.strip()
        # item['url'] = url
        # item['deadline'] = ...
        return item

    def crawl(self):
        current_page = 1
        queue = list(self.start_urls)

        while queue and current_page <= self.max_pages:
            list_url = queue.pop(0)
            if list_url in self.visited_urls:
                continue
            self.visited_urls.add(list_url)

            print(f"Fetching list page: {list_url}")
            list_html = self.fetch_page(list_url)
            if not list_html:
                continue

            # Find links to detail pages
            # for detail_url in self.parse_listings(list_html):
            #     if detail_url in self.visited_urls: continue
            #     self.visited_urls.add(detail_url)
            #
            #     print(f"  Fetching detail: {detail_url}")
            #     detail_html = self.fetch_page(detail_url)
            #     if detail_html:
            #         art_call = self.parse_detail_page(detail_html, detail_url)
            #         if art_call:
            #             yield art_call
            #     time.sleep(1) # Be respectful

            # Find next page link (if any)
            # ... soup.select_one("a.next-page") ...
            # if next_page_url and current_page < self.max_pages:
            #    queue.append(next_page_url)
            #    current_page += 1

            time.sleep(2) # Be respectful

# To run this spider
# if __name__ == '__main__':
#     spider = CallForEntrySpider(max_pages=2)
#     for item in spider.crawl():
#         print(item)
