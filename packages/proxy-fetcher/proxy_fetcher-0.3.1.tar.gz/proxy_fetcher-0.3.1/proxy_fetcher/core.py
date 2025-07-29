import asyncio
import aiohttp
import requests
from tqdm.asyncio import tqdm_asyncio
from typing import Callable, Optional

DEFAULT_SETTINGS = {
    'MIN_WORKING_PROXIES': 5,
    'PROXY_LIMIT': 200,
    'TIMEOUT': 10,
    'MAX_ATTEMPTS': 3,
    'CONCURRENT_CHECKS': 350,
    'TEST_URLS': [
        "http://httpbin.org/ip",
        "http://icanhazip.com",
        "http://api.ipify.org"
    ],
    'CUSTOM_TEST_URL': None,
    'CUSTOM_VALIDATOR': None,
    'USER_AGENT': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

class ProxyFetcher:
    def __init__(self, **kwargs):
        self.settings = DEFAULT_SETTINGS.copy()
        self.settings.update(kwargs)
        
        self.min_working = self.settings['MIN_WORKING_PROXIES']
        self.proxy_limit = self.settings['PROXY_LIMIT']
        self.timeout = self.settings['TIMEOUT']
        self.max_attempts = self.settings['MAX_ATTEMPTS']
        self.concurrent_checks = self.settings['CONCURRENT_CHECKS']
        self.test_urls = self.settings['TEST_URLS']
        self.custom_url = self.settings['CUSTOM_TEST_URL']
        self.custom_validator = self.settings['CUSTOM_VALIDATOR']
        self.user_agent = self.settings['USER_AGENT']
        
        self.working_proxies = []
        self.semaphore = None
    
    def get_proxies(self):
        """Получает прокси с нескольких источников (синхронно)"""
        sources = [
            f"https://proxylist.geonode.com/api/proxy-list?limit={self.proxy_limit}&page=1",
            "https://api.proxyscrape.com/v2/?request=displayproxies",
            "http://free-proxy.cz/en/proxylist/country/all/https/ping/all"
        ]
        
        proxies = []
        for url in sources:
            try:
                response = requests.get(url, timeout=15)
                if "geonode" in url:
                    proxies.extend([f"{p['ip']}:{p['port']}" for p in response.json().get("data", [])])
                else:
                    proxies.extend(response.text.strip().split('\r\n'))
            except Exception as e:
                print(f"Ошибка при получении прокси из {url}: {str(e)}")
                continue
        
        return list(set(proxies))

    async def _check_proxy(self, session, proxy_str):
        """Асинхронная проверка одного прокси"""
        # Выбираем URL для проверки
        if self.custom_url:
            test_urls = [self.custom_url]
        else:
            test_urls = self.test_urls
            
        proxy_url = f"http://{proxy_str}"
        headers = {'User-Agent': self.user_agent}
        
        for test_url in test_urls:
            try:
                async with session.get(
                    test_url,
                    proxy=proxy_url,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                    ssl=False
                ) as response:
                    content = await response.text()
                    
                    # Кастомная проверка
                    if self.custom_validator:
                        if self.custom_validator(response, content):
                            return proxy_str
                    # Стандартная проверка
                    elif response.status == 200:
                        return proxy_str
            except Exception as e:
                continue
        return None

    async def _check_proxies_batch(self, proxies):
        """Проверяет пакет прокси асинхронно"""
        connector = aiohttp.TCPConnector(limit_per_host=self.concurrent_checks)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [self._check_proxy(session, proxy) for proxy in proxies]
            results = await tqdm_asyncio.gather(
                *tasks,
                desc="Проверка прокси",
                total=len(tasks),
                ascii=True,
                ncols=75
            )
            return [result for result in results if result]

    async def _fetch_proxies_async(self):
        """Асинхронная основная логика получения прокси"""
        attempts = 0
        
        while len(self.working_proxies) < self.min_working and attempts < self.max_attempts:
            attempts += 1
            print(f"\nПопытка {attempts}/{self.max_attempts}. Получаем прокси...")
            
            proxies = self.get_proxies()
            if not proxies:
                print("Не удалось получить прокси. Повторяем...")
                continue
                
            print(f"Получено {len(proxies)} прокси. Начинаем проверку...")
            
            # Разбиваем на батчи для оптимизации
            batch_size = min(len(proxies), self.concurrent_checks * 2)
            for i in range(0, len(proxies), batch_size):
                batch = proxies[i:i + batch_size]
                working_batch = await self._check_proxies_batch(batch)
                self.working_proxies.extend(working_batch)
                
                if len(self.working_proxies) >= self.min_working:
                    break
            
            print(f"Найдено рабочих: {len(self.working_proxies)}/{self.min_working}")
        
        if self.working_proxies:
            with open('working_proxies.txt', 'w') as f:
                f.write('\n'.join(self.working_proxies))
            print(f"\nУспех! Сохранено {len(self.working_proxies)} рабочих прокси.")
            return True
        else:
            print("\nНе удалось найти рабочие прокси.")
            return False

    def fetch_proxies(self):
        """Синхронный интерфейс для асинхронной операции"""
        return asyncio.run(self._fetch_proxies_async())

def get_proxies(
    custom_url: Optional[str] = None,
    custom_validator: Optional[Callable[[aiohttp.ClientResponse, str], bool]] = None,
    user_agent: Optional[str] = None,
    **kwargs
):
    """
    Quick access function to get working proxies with custom testing
    
    Args:
        custom_url: Specific URL to test proxies against
        custom_validator: Function to validate response (receives response and content)
        user_agent: Custom User-Agent header
        **kwargs: Other configuration options
        
    Returns:
        list: List of working proxies in 'ip:port' format
    """
    fetcher = ProxyFetcher(
        CUSTOM_TEST_URL=custom_url,
        CUSTOM_VALIDATOR=custom_validator,
        USER_AGENT=user_agent or DEFAULT_SETTINGS['USER_AGENT'],
        **kwargs
    )
    success = fetcher.fetch_proxies()
    return fetcher.working_proxies if success else []