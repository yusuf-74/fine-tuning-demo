import asyncio
import aiohttp
import json
from bs4 import BeautifulSoup

urls = {}
with open('urls.json') as f:
    urls = json.load(f)

urls = urls['elected_urls']+urls['social_media_urls']+urls['side_websites']


async def fetch_paragraphs(semaphore, session, url):
    async with semaphore:
        async with session.get(url) as response:
            content = await response.content.read()
            html = content.decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html, 'html.parser')
            paragraphs = [p.text for p in soup.find_all('p')]
            return paragraphs

async def main(urls):
    semaphore = asyncio.Semaphore(30)  # limit to 10 concurrent requests
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_paragraphs(semaphore, session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

if __name__ == '__main__':
    # results = asyncio.run(main(urls[:500]))
    # with open('paragraphs.json','w') as f:
    #     json.dump(results,f,indent=4)  
    
    rest_of_results = asyncio.run(main(urls[500:620]))
    with open('paragraphs2.json','w') as f:
        json.dump(rest_of_results,f,indent=4)