#!/usr/bin/env python
import time
import json
import requests
import aiohttp
import asyncio
from datetime import datetime
from asyncio import create_task
from pprint import pprint
from config import FINNHUB_TOKEN as TOKEN, API

class Session:
    def __init__(self):
        self.session = {}

    async def start(self):
        self._session = aiohttp.ClientSession()

    async def close(self):
        await self._session.close()

    async def fetch(self, url):
        try:
            async with self._session.get(url, verify_ssl=False) as resp:
                return await resp.json()
        except Exception as e:
            print(f'Unable to send request for {url} Due to {e}')
    

client = Session()

async def main():
    await client.start()
    start = time.perf_counter()

    # Run the coroutines concurrently
    fetch_tech = create_task(fetch_tech_news(API))
    fetch_mergers = create_task(fetch_merger_news(API))

    tech_articles = await fetch_tech
    merger_articles = await fetch_mergers

    def generate_files():
        write_file("tech_news.txt", tech_articles)
        write_file("merger_news.txt", merger_articles)

    generate_files()

    stop = time.perf_counter()
    duration = (stop - start)

    print(f"Finished fetching articles in {duration:.2f}secs")
    await client.close()

async def fetch_tech_news(url, category='general'):
    resp = await client.fetch(f'{url}/news?category={category}&token={TOKEN}')
    filtered_articles = []

    for article in resp:
        if article['category'] in ('business', 'technology', 'finance'):
            filtered_articles.append(article)
    return filtered_articles

async def fetch_merger_news(url, category='merger'):
    resp = await client.fetch(f'{url}/news?category={category}&token={TOKEN}')
    return resp

def write_file(filename, arr):
    header = filename.split("_")[0]
    with open(filename, "w+") as f_obj:
        f_obj.write(f'{header.upper()} News:\n\n')
        for article in arr:
            f_obj.write(f"""Headline: {article['headline']}\n
Link: {article['url']}\n
Date: {datetime.fromtimestamp(article['datetime'])}\n\n
""")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


