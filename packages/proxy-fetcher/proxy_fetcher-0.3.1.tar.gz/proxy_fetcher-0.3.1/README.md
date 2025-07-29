Proxy Fetcher (Enhanced)

Python package for fetching and validating HTTP/HTTPS proxies from multiple sources with asynchronous support and custom validation.
Features

    Asynchronous validation for high-performance proxy checking

    Custom URL testing - verify proxies against specific websites

    Advanced validation with custom response validators

    User-Agent customization to avoid blocking

    Multiple proxy sources (Geonode, ProxyScrape, Free-Proxy.CZ)

    Progress tracking with tqdm

    Automatic saving of working proxies

Installation
bash

pip install proxy-fetcher

    Note: Requires Python 3.13 or higher

Quick Start
Basic Usage
python

from proxy_fetcher import get_proxies

# Get 10 working proxies (default)
proxies = get_proxies()
print(f"Found {len(proxies)} working proxies")

Custom URL Testing
python

# Test proxies against a specific website
proxies = get_proxies(
    custom_url="https://www.google.com/finance/quote/AED-KZT",
    timeout=8
)

Advanced Validation
python

def custom_validator(response, content):
    # Validate response content
    return "AED-KZT" in content and response.status == 200

proxies = get_proxies(
    custom_url="https://www.google.com/finance/quote/AED-KZT",
    custom_validator=custom_validator,
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
)

Performance Tuning
python

proxies = get_proxies(
    CONCURRENT_CHECKS=200,  # Parallel checks (default: 100)
    TIMEOUT=3,              # Shorter timeout for faster results
    PROXY_LIMIT=500,        # More proxies to test
    MAX_ATTEMPTS=5          # More attempts to find proxies
)

Configuration Options
Parameter	Default	Description
MIN_WORKING_PROXIES	10	Minimum working proxies to find
PROXY_LIMIT	100	Max proxies to fetch per attempt
TIMEOUT	5	Timeout for proxy validation (seconds)
MAX_ATTEMPTS	3	Max attempts to reach target count
CONCURRENT_CHECKS	100	Number of concurrent proxy checks (increase for speed)
TEST_URLS	Standard list	Default URLs for proxy validation
CUSTOM_TEST_URL	None	Specific URL to test proxies against (overrides TEST_URLS)
CUSTOM_VALIDATOR	None	Custom function to validate proxy response (see example)
USER_AGENT	Modern browser	User-Agent header to use for validation requests
Advanced Usage
Using the ProxyFetcher Class
python

from proxy_fetcher import ProxyFetcher

fetcher = ProxyFetcher(
    MIN_WORKING_PROXIES=5,
    CUSTOM_TEST_URL="https://example.com",
    CONCURRENT_CHECKS=250,
    USER_AGENT="My Custom User Agent"
)

if fetcher.fetch_proxies():
    print(f"Working proxies: {fetcher.working_proxies}")
    # Save to custom file
    with open('my_proxies.txt', 'w') as f:
        f.write('\n'.join(fetcher.working_proxies))

Custom Validator Examples

For Google Finance:
python

def google_finance_validator(response, content):
    # Check status and content
    return response.status == 200 and "AED-KZT" in content and "currency exchange rate" in content

For JSON APIs:
python

import json

def json_api_validator(response, content):
    try:
        data = json.loads(content)
        return data.get("success") and response.status == 200
    except:
        return False

Proxy Storage
Automatic Saving

Working proxies are automatically saved to working_proxies.txt after successful validation.
Manual Export
python

proxies = get_proxies()
with open('custom_proxies.txt', 'w') as f:
    f.write('\n'.join(proxies))

Loading Proxies
python

with open('working_proxies.txt') as f:
    loaded_proxies = f.read().splitlines()

## Performance Tips

    Increase concurrency: Set CONCURRENT_CHECKS=200-500 for faster validation

    Reduce timeout: Set TIMEOUT=3-5 seconds for public proxies

    Custom validation: Implement specific checks for target websites

    Use fresh proxies: Public proxies often have short lifespans

## Troubleshooting

    No proxies found:

        Increase TIMEOUT (10-15 seconds)

        Use simpler TEST_URLS (like http://httpbin.org/ip)

        Increase MAX_ATTEMPTS

    Slow validation:

        Increase CONCURRENT_CHECKS

        Reduce PROXY_LIMIT

    Blocked by target site:

        Rotate User-Agents

        Add delays between requests

License

MIT
Changelog (v0.3.0)

    Added asynchronous validation with aiohttp

    Implemented custom URL testing

    Added support for response validators

    Enhanced User-Agent customization

    Improved performance with concurrent checks

    Updated documentation with Google Finance examples

    For support and issues, visit GitHub Repository

## Совместимость

Пакет работает с Python 3.11 и выше. Для использования с Python 3.11 установите:

```bash
pip install proxy-fetcher==0.3.1