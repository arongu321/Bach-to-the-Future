import requests
from bs4 import BeautifulSoup
import time

def get_page(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        if len(list(soup.children)) < 3:
            print('Invalid response, wait 5s')
            time.sleep(5)
            page = requests.get(url)  # try again if the response was incorrect
            soup = BeautifulSoup(page.content, 'html.parser')

            if len(list(soup.children)) < 3:
                print('Still invalid, giving up')
                return None
        return soup
    except:
        return None