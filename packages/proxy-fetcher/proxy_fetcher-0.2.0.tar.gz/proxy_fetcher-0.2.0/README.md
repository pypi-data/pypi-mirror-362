# Proxy Fetcher

Python package for fetching and validating HTTP/HTTPS proxies from multiple sources.

## Features
- Automatic proxy validation
- Multiple sources (Geonode, ProxyScrape, etc.)
- Customizable parameters
- Progress bar with `tqdm`

## Installation
```bash
pip install proxy-fetcher
```

# Quick Start

``` python
from proxy_fetcher import get_proxies

# Get 10 working proxies (default)
proxies = get_proxies()
print(f"Found {len(proxies)} working proxies")

# Custom settings
proxies = get_proxies(
    MIN_WORKING_PROXIES=15,
    PROXY_LIMIT=50,
    TIMEOUT=10
)
```

# Advanced Usage

``` python
from proxy_fetcher import ProxyFetcher

# Manual control
fetcher = ProxyFetcher(
    MIN_WORKING_PROXIES=5,
    TEST_URLS=["http://my-site.com/check-ip"]
)

if fetcher.fetch_proxies():
    print(fetcher.working_proxies)
```

# Configuration Options

| Parameter            | Default | Description                          |
|----------------------|---------|--------------------------------------|
| `MIN_WORKING_PROXIES` | 10     | Minimum working proxies to find      |
| `PROXY_LIMIT`        | 100     | Max proxies to fetch per attempt     |
| `TIMEOUT`            | 5       | Timeout for validation (seconds)     |
| `MAX_ATTEMPTS`       | 3       | Max attempts to reach target count   |
| `TEST_URLS`          | See below | URLs for proxy validation           |

## Proxy Storage

### Save proxies to file:
```python
from proxy_fetcher import get_proxies

proxies = get_proxies()
with open('proxies.txt', 'w') as f:
    f.write('\n'.join(proxies))
```

### Load proxies from file:
```python
with open('proxies.txt') as f:
    loaded_proxies = f.read().splitlines()
```

# License

MIT