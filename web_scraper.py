from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import validators
import time
import json

# Elected URLs
elected_urls = []

# Social media URLs
social_media_urls = []

# Side Websites
side_websites = []

social_media_domains = ['facebook', 'twitter', 'instagram', 'youtube', 'linkedin']

visited_urls = set()

def get_important_links(url , depth):
    if url in visited_urls:
        return
    
    if depth == 3:
        return
    
    visited_urls.add(url)
    # get domain name 
    domain = url.split('.')[1]
    
    if domain in social_media_domains:
        social_media_urls.append(url)
        return
    
    # check if url is valid
    if not validators.url(url):
        return
    
    # get html
    links_to_be_checked = []
    try:
        with urlopen(url) as response:
            body = response.read()
            page = BeautifulSoup(body,'html.parser')
            
            # get all links
            for link in page.find_all('a'):
                link = link.get('href')
                if link is None:
                    continue
                if link.startswith('http'):
                    links_to_be_checked.append(link)
                else:
                    if link.startswith('/'):
                        links_to_be_checked.append('https://www.torontomu.ca' + link)
                    else:
                        continue
    except urllib.error.HTTPError as e:
        pass
    for link in links_to_be_checked:
        if link in elected_urls or link in social_media_urls or link in side_websites:
            continue
        else:
            if link.startswith('https://www.torontomu.ca/'):
                elected_urls.append(link)
                
                get_important_links(link, depth + 1)
            else:
                side_websites.append(link)
    return

get_important_links('https://www.torontomu.ca/',0)

with open('urls.json','w') as f:
    urls = {
        'elected_urls': elected_urls,
        'social_media_urls': social_media_urls,
        'side_websites': side_websites
    }
    json.dump(urls,f)