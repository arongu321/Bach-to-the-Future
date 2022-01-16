import requests
from bs4 import BeautifulSoup
from util import get_page
import json

def get_fbm_page_info(url):
    category = url[22:].split('/')[0]
    soup = get_page(url)

    if not soup:
        return None

    try:
        price = None
    except:
        price = None

    try:
        currency = None
    except:
        currency = None

    try:
        title = None
    except:
        title = None

    try:
        content = json.loads(soup.find_all('script')[1].get_text())['description']
        #.split(':')[7]
        #.split('"')[1]
    except:
        content = None

    listing_type = None
    date = None

    return {'price': [price, currency, listing_type], 'title': title, 'category': category, 'content': content,
            'date': date}

if __name__ == "__main__":
    url = "https://www.facebook.com/marketplace/item/4529181560527923"

    print(get_fbm_page_info(url)['content'])
