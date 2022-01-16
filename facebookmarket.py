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
        price = json.loads(soup.find_all('script')[1].get_text())['offers']['price']
    except:
        price = None

    try:
        currency = json.loads(soup.find_all('script')[1].get_text())['offers']['priceCurrency']
    except:
        currency = None

    try:
        title = json.loads(soup.find_all('script')[1].get_text())['name']
    except:
        title = None

    try:
        content = json.loads(soup.find_all('script')[1].get_text())['description']
    except:
        content = None

    date = None

    listing_type = None

    return {'price': [price, currency, listing_type], 'title': title, 'category': category, 'content': content,
            'date': date}

if __name__ == "__main__":
    url = "https://www.facebook.com/marketplace/item/205016458501904"
    print(get_fbm_page_info(url))
