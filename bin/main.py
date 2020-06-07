#!/usr/bin/env python3.7
import os
import time
import json
import requests
import aiohttp
import asyncio
from datetime import datetime
from asyncio import create_task
from pprint import pprint
from config import FINNHUB_TOKEN as TOKEN, API, NEWS_API_KEY

SOURCES = "https://newsapi.org/v2/sources"

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

class Session:
    def __init__(self):
        self.session = {}

    async def start(self):
        self._session = aiohttp.ClientSession()

    async def close(self):
        await self._session.close()

    async def fetch(self, url, headers=None):
        try:
            async with self._session.get(url, headers=headers, verify_ssl=False) as resp:
                return await resp.json()
        except Exception as e:
            print(f'Unable to send request for {url} Due to {e}')
    

client = Session()

async def main():
    await client.start()
    start = time.perf_counter()

    # Run the coroutines concurrently
    # fetch_mergers = create_task(fetch_merger_news(API))
    # merger_articles = await fetch_mergers
    fetch_tech_sources = create_task(fetch_technology_sources(SOURCES))
    tech_news = create_task(fetch_technology_news("https://newsapi.org/v2/top-headlines?category=technology&language=en"))
    tech_articles = await tech_news

    def generate_files():
        write_file(f"{DIR_PATH}/tech_news.txt", tech_articles)
        write_file(f"{DIR_PATH}/merger_news.txt", merger_articles)

    generate_files()

    stop = time.perf_counter()
    duration = (stop - start)

    print(f"Finished fetching articles in {duration:.2f}secs")
    await client.close()

async def fetch_merger_news(url, category='merger'):
    resp = await client.fetch(f'{url}/news?category={category}&token={TOKEN}')
    return resp

async def fetch_technology_sources(url, category='technology'):
    headers = {'Authorization': f"Bearer {NEWS_API_KEY}"}
    resp = await client.fetch(url, headers)

    return resp

async def fetch_technology_news(url, category='technology'):
    headers = {'Authorization': f"Bearer {NEWS_API_KEY}"}
    resp = await client.fetch(url, headers)
    articles = []

    for article in resp['articles']:
        for attempt in range(1):
            try:
                if article['description']:
                    article['description'].encode('utf-8').decode('ascii')
            except UnicodeDecodeError:
                break
            else:
                if article not in articles:
                    articles.append(article)
    return articles


def write_file(filename, arr):
    header = filename.split("/")[-1].split("_")[0]
    with open(filename, "w+") as f_obj:
        f_obj.write(f'<h3 style="margin-left: 20px;">Daily {header.title()} News:</h3>\n\n')
        for article in arr:
            date = article['publishedAt'].split("T")
            title = article['title'].split(" ")
            f_obj.write(f"""<div style="margin-left: 20px;"><a href="{article['url']}">{article['title']}</a><br>
<strong>{date[0]} {date[1][:-1]}</strong><br><br>
</div>
""")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


