import requests
from bs4 import BeautifulSoup
from util import get_page

def get_fbm_page_info(url):

    soup = get_page(url)
    '''
    for title in soup.find_all('title'):
        print(title.get_text())
    '''
    if not soup:
        return None
    print(soup)
    
if __name__ == "__main__":
    url = "https://www.facebook.com/marketplace/item/355095496002798"

    get_fbm_page_info(url)

    
