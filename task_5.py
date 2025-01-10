import json
import asyncio

import aiohttp

from unittest.mock import Mock



urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url"
]


async def fetch(session:aiohttp.ClientSession, url):
    try:
        async with session.get(url, ssl=False) as response:
            return {url: response.status}
    except aiohttp.ConnectionTimeoutError:
        return {url: 0}
    except aiohttp.ClientError:
        return {url: 0}
    

async def fetch_urls(urls: list[str], file_path: str):
    semaphore = asyncio.Semaphore(5)
    async with aiohttp.ClientSession() as session:
        data = [await fetch_with_semaphore(session, url, semaphore) for url in urls]

        with open(file_path, 'w') as f:
            f.write(json.dumps(data))
        return data
        

async def fetch_with_semaphore(session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore) -> dict:
    async with semaphore:
        return await fetch(session, url)
    



if __name__ == '__main__':
    mock = Mock(return_value=[{"https://example.com": 200}, {"https://httpbin.org/status/404": 404}, {"https://nonexistent.url": 0}])
    
    assert asyncio.run(fetch_urls(urls, './results.json')) == mock
