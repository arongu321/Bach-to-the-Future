import requests
from bs4 import BeautifulSoup
from util import get_page

def get_fbm_page_info(url):
    category = url[22:].split('/')[0]

    soup = get_page(url)
    for title in soup.find_all('title'):
        print(title.get_text())

    print(str(soup))

    if not soup:
        return None

    try:
        html = list(soup.children)[2]
        head = list(html.children)[1]
        body = list(html.children)[3]
    except:
        return None
    print(body)

if __name__ == "__main__":
    url = "https://www.facebook.com/marketplace/item/355095496002798"

    get_fbm_page_info(url)