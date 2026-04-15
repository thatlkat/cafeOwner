# [e.g., nyfa_spider.py]
import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin, urlparse

# --- Filters ---
DOMAIN_BLACKLIST = {
    "exhibizone.com",
}

def should_skip_url(url):
    try:
        domain = urlparse(url).netloc.lower()
        return any(blacklisted in domain for blacklisted in DOMAIN_BLACKLIST)
    except Exception:
        return True # Skip malformed URLs

def is_likely_vanity_or_pay_to_play(soup):
    text = soup.get_text().lower()
    vanity_keywords = [
        "exhibition fee", "participation fee", "hanging fee",
        "guaranteed exhibition", "all artists will be featured",
        "pay to show", "artist fee: $", "entry fee: $"
    ]
    if any(keyword in text for keyword in vanity_keywords):
        return True

    # High application/entry fees (example threshold)
    fee_patterns = re.compile(r"(application fee|entry fee):? *\$(\d+(\.\d{2})?)")
    matches = fee_patterns.findall(text)
    for match in matches:
        try:
            if float(match[1]) > 75.00:  # Example threshold
                print(f"Note: Potential high fee found: ${match[1]}")
                # Decide if this automatically means pay-to-play
                # return True
        except ValueError:
            pass
    return False

def is_internet_only(soup):
    text = soup.get_text().lower()
    online_keywords = [
        "online only", "virtual gallery", "digital exhibition",
        "website exhibition", "no physical space", "exclusively online"
    ]
    if any(keyword in text for keyword in online_keywords):
        return True
    return False

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

# --- End Filters ---

def scrape_site(site_name="Example Site", base_url="https://example.com"):
    print(f"Scraping {site_name}...")
    opportunities = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 ArtCallAggregator/1.0'
    }

    try:
        # TODO: Adjust the starting URL to the actual opportunities page
        start_url = base_url
        response = requests.get(start_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # TODO: Identify how to find links to individual opportunity listings
        # Example: links = soup.select("a.opportunity-link")
        listing_links = [] # Placeholder

        for link in listing_links:
            opportunity_url = urljoin(base_url, link['href'])
            if should_skip_url(opportunity_url):
                print(f"Skipping blacklisted URL: {opportunity_url}")
                continue

            print(f"  Fetching: {opportunity_url}")
            time.sleep(1) # Be respectful
            try:
                detail_response = requests.get(opportunity_url, headers=headers, timeout=10)
                detail_response.raise_for_status()
                detail_soup = BeautifulSoup(detail_response.content, 'html.parser')

                if is_likely_vanity_or_pay_to_play(detail_soup):
                    print(f"  Skipping likely vanity/pay-to-play: {opportunity_url}")
                    continue
                if is_internet_only(detail_soup):
                    print(f"  Skipping online-only: {opportunity_url}")
                    continue

                # TODO: Extract specific data from the detail_soup
                title = clean_text(detail_soup.find('h1').text) if detail_soup.find('h1') else "No Title"
                # description = ...
                # deadline = ...
                # location = ...
                # eligibility = ...

                opportunities.append({
                    "title": title,
                    "url": opportunity_url,
                    "source": site_name,
                    # Add other extracted fields
                })

            except requests.exceptions.RequestException as e:
                print(f"  Error fetching detail page {opportunity_url}: {e}")
            except Exception as e:
                print(f"  Error processing detail page {opportunity_url}: {e}")

        # TODO: Implement pagination if necessary

    except requests.exceptions.RequestException as e:
        print(f"Error fetching site {site_name}: {e}")
    except Exception as e:
        print(f"Error scraping site {site_name}: {e}")

    return opportunities

if __name__ == '__main__':
    # This is a placeholder. Replace with specific site info in each file.
    # SITE_NAME = "Example"
    # BASE_URL = "https://example.com"
    # results = scrape_site(SITE_NAME, BASE_URL)
    # print(f"Found {len(results)} opportunities on {SITE_NAME}.")
    # for opp in results:
    #     print(f"  - {opp['title']}: {opp['url']}")
    pass
