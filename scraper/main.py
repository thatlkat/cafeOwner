# main.py

import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse, urljoin
import re
import json

# --- Configuration ---
DOMAIN_BLACKLIST = {
    "exhibizone.com",
}

VANITY_KEYWORDS = [
    "exhibition fee", "participation fee", "hanging fee",
    "guaranteed exhibition", "all artists will be featured",
    "pay to show", "artist fee", "cooperative gallery", "membership to exhibit"
]
HIGH_FEE_THRESHOLD = 75.00  # Example threshold for application fees

ONLINE_ONLY_KEYWORDS = [
    "online only", "virtual gallery", "digital exhibition",
    "website exhibition", "no physical space", "e-exhibit", "metaverse"
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

REQUEST_DELAY = 2  # Seconds to wait between requests

# --- Helper Functions ---
def fetch_page(url):
    """Fetches the content of a URL."""
    print(f"Fetching: {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=20)
        response.raise_for_status()
        time.sleep(REQUEST_DELAY)  # Respectful delay
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def should_skip_domain(url):
    """Checks if the URL's domain is blacklisted."""
    try:
        domain = urlparse(url).netloc.lower()
        for blacklisted in DOMAIN_BLACKLIST:
            if blacklisted in domain:
                print(f"Skipping blacklisted domain: {domain} from {url}")
                return True
        return False
    except Exception as e:
        print(f"Error parsing URL {url}: {e}")
        return True

def is_likely_vanity_or_pay_to_play(soup, url):
    """Checks for signs of vanity or pay-to-play schemes."""
    text = soup.get_text().lower()
    if any(keyword in text for keyword in VANITY_KEYWORDS):
        print(f"Vanity keyword found on {url}")
        return True

    try:
        fee_patterns = re.compile(r"(?:application fee|entry fee|submission fee):? *\$(\d+(?:\.\d{2})?)")
        matches = fee_patterns.findall(text)
        for match in matches:
            try:
                if float(match) > HIGH_FEE_THRESHOLD:
                    print(f"High fee (${match}) found on {url}")
                    return True
            except ValueError:
                pass
    except Exception as e:
        print(f"Error checking fees on {url}: {e}")
    return False

def is_internet_only(soup, url):
    """Checks if the exhibit is likely online-only."""
    text = soup.get_text().lower()
    if any(keyword in text for keyword in ONLINE_ONLY_KEYWORDS):
        print(f"Online-only keyword found on {url}")
        return True
    # Could add checks for absence of physical address if necessary
    return False

def extract_call_details(soup, url):
    """
    Extracts information about the art call from the parsed HTML.
    THIS FUNCTION IS SITE-SPECIFIC. You need to inspect the HTML structure
    of the website you are scraping and adjust the BeautifulSoup selectors.
    """
    details = {"url": url, "source_site": urlparse(url).netloc}

    # Example for callforentry.org detail pages (NEEDS VERIFICATION AND ADJUSTMENT)
    try:
        title_tag = soup.find('h1')
        details["title"] = title_tag.get_text(strip=True) if title_tag else "No title found"

        # Example: looking for deadline
        # deadline_el = soup.find('span', {'id': 'deadline'})
        # if deadline_el:
        #     details['deadline'] = deadline_el.get_text(strip=True)

        # Add more extraction logic for:
        # - Deadline
        # - Location (City, State, Country)
        # - Description / Call text
        # - Eligibility
        # - How to apply link
        # - Organizer

        # This is a placeholder - replace with actual extraction logic
        print(f"Extracted: {details['title']} from {url}")
        return details
    except Exception as e:
        print(f"Error extracting details from {url}: {e}")
        return None

def find_call_links(list_url):
    """
    Finds individual call links from a listing page.
    THIS IS SITE-SPECIFIC.
    """
    html_content = fetch_page(list_url)
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    base_url = f"{urlparse(list_url).scheme}://{urlparse(list_url).netloc}"

    # Example for callforentry.org festival listing page (NEEDS ADJUSTMENT)
    # Inspect the page to find the correct selectors for links to individual calls
    for link_tag in soup.find_all('a', href=True):
        href = link_tag['href']
        if 'festivals_detail.php?id=' in href:
            full_url = urljoin(base_url, href)
            if full_url not in links:
                links.append(full_url)

    print(f"Found {len(links)} potential call links on {list_url}")
    return links

# --- Main Scraper Logic ---
def process_call_url(url):
    """Fetches, parses, filters, and extracts details from a single call URL."""
    if should_skip_domain(url):
        return None

    html_content = fetch_page(url)
    if not html_content:
        return None

    soup = BeautifulSoup(html_content, 'html.parser')

    if is_likely_vanity_or_pay_to_play(soup, url):
        print(f"Filtering out (Vanity/Pay-to-Play): {url}")
        return None

    if is_internet_only(soup, url):
        print(f"Filtering out (Online-Only): {url}")
        return None

    call_info = extract_call_details(soup, url)
    return call_info

# --- Entry Point ---
if __name__ == "__main__":
    print("Starting scraper...")

    callforentry_list_url = "https://www.callforentry.org/festivals.php"
    collected_calls = []

    print(f"\n--- Finding call links from: {callforentry_list_url} ---")
    individual_call_urls = find_call_links(callforentry_list_url)

    # Limit for testing purposes
    # individual_call_urls = individual_call_urls[:5]

    for i, call_url in enumerate(individual_call_urls):
        print(f"\n--- Processing call {i+1}/{len(individual_call_urls)}: {call_url} ---")
        call_details = process_call_url(call_url)
        if call_details:
            collected_calls.append(call_details)
            print(f"VALID CALL ADDED: {call_details['title']}")

    # TODO: Save the collected_calls to a file or database
    if collected_calls:
        try:
            with open("art_calls.json", "w") as f:
                json.dump(collected_calls, f, indent=2)
            print(f"\nSaved {len(collected_calls)} valid calls to art_calls.json")
        except Exception as e:
            print(f"Error saving results: {e}")
    else:
        print("\nNo valid calls were collected.")

    print("\nScraper finished.")
