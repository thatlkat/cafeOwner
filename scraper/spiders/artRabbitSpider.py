import scrapy
from art_call_aggregator.items import ArtCallItem
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re

class ArtRabbitSpider(scrapy.Spider):
    name = 'artrabbit'
    allowed_domains = ['artrabbit.com']
    # NOTE: Adjust start_urls to the actual page listing opportunities or open calls.
    # This URL is a guess and might need to be changed.
    start_urls = ['https://www.artrabbit.com/artist-opportunities']

    # --- Filters ---
    DOMAIN_BLACKLIST = {"exhibizone.com"}
    HIGH_FEE_THRESHOLD = 75.00

    def should_skip_url(self, url):
        try:
            domain = urlparse(url).netloc.lower()
            return any(blacklisted in domain for blacklisted in self.DOMAIN_BLACKLIST)
        except Exception:
            return True # Skip malformed URLs

    def is_likely_vanity_or_pay_to_play(self, soup):
        text = soup.get_text().lower()
        vanity_keywords = [
            "exhibition fee", "participation fee", "hanging fee",
            "guaranteed exhibition", "all artists will be featured",
            "pay to show",
        ]
        if any(keyword in text for keyword in vanity_keywords):
            self.logger.info(f"Vanity keyword found on {self.current_url}")
            return True

        try:
            fee_patterns = re.compile(r"(application fee|entry fee|submission fee):? *\$(\d+(?:\.\d{2})?)")
            matches = fee_patterns.findall(text)
            for match in matches:
                try:
                    if float(match[1]) > self.HIGH_FEE_THRESHOLD:
                         self.logger.info(f"High fee (${match[1]}) found on {self.current_url}")
                         # Context is important, but high fees are a flag.
                         # Consider adding more checks, e.g., if not clearly juried.
                         # For now, let's flag it.
                         return True
                except ValueError:
                    pass
        except Exception as e:
            self.logger.error(f"Error checking fees on {self.current_url}: {e}")
        return False

    def is_internet_only(self, soup):
        text = soup.get_text().lower()
        online_keywords = [
            "online only", "virtual gallery", "digital exhibition",
            "website exhibition", "no physical space", "exclusively online"
        ]
        if any(keyword in text for keyword in online_keywords):
            self.logger.info(f"Online-only keyword found on {self.current_url}")
            return True
        return False
    # --- End Filters ---

    def parse(self, response):
        self.logger.info(f"Parsing list page: {response.url}")

        # --- TODO: Find links to individual opportunity pages ---
        # --- Inspect ArtRabbit to find the correct CSS or XPath selectors ---
        # Example placeholder selectors:
        opportunity_links = response.css('div.opportunity-card a::attr(href)').getall()
        # opportunity_links = response.xpath('//a[contains(@class, "opportunity-link")]/@href').getall()

        if not opportunity_links:
            self.logger.warning(f"No opportunity links found on {response.url} with current selectors")

        for link in opportunity_links:
            detail_url = response.urljoin(link)
            if self.should_skip_url(detail_url):
                self.logger.info(f"Skipping blacklisted domain: {detail_url}")
                continue
            yield scrapy.Request(detail_url, callback=self.parse_opportunity_details)

        # --- TODO: Handle Pagination ---
        # --- Inspect ArtRabbit for next page links ---
        # Example placeholder:
        # next_page = response.css('a.next-page::attr(href)').get()
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)

    def parse_opportunity_details(self, response):
        self.current_url = response.url
        self.logger.info(f"Parsing detail page: {response.url}")

        # Use BeautifulSoup for easier text extraction and filter checks
        soup = BeautifulSoup(response.text, 'html.parser')

        if self.is_likely_vanity_or_pay_to_play(soup):
            return
        if self.is_internet_only(soup):
            return

        item = ArtCallItem()
        item['url'] = response.url
        item['source_site'] = 'artrabbit.com'

        # --- TODO: Extract item fields using CSS or XPath selectors for ArtRabbit ---
        item['title'] = response.css('h1.opportunity-title::text').get() or response.xpath('//h1[@class="opportunity-title"]/text()').get()
        item['organization'] = response.css('div.org-name a::text').get()
        item['description'] = " ".join(response.css('div.opportunity-description ::text').getall()).strip()

        # Example for deadline - highly site specific
        item['deadline'] = response.css('span.deadline-date::text').get()

        item['location'] = response.css('span.location-text::text').get()
        # item['application_fee'] = ...
        # item['eligibility'] = ...

        # Clean up extracted data
        for field in item.fields:
            if isinstance(item.get(field), str):
                item[field] = item[field].strip()

        if item.get('title'):
            yield item
        else:
            self.logger.warning(f"Could not extract title from {response.url}")


