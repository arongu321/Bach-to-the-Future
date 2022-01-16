import requests
from bs4 import BeautifulSoup
from util import get_page
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from storageBoi import StorageBoi
from tqdm import tqdm
from selenium.webdriver.firefox.options import Options

def get_fbm_page_info(url):
    category = url[22:].split('/')[0]
    soup = get_page(url)

    if not soup:
        return None

    try:
        price = float(json.loads(soup.find_all('script')[1].get_text())['offers']['price'])
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

def make_fbm_search_url(search_string, region='edmonton', ):
    #search_string = search_string.lower().replace(' ', '-')

    region = region.lower()

    url = "https://www.facebook.com/marketplace/" + region + "/search/?query=" + search_string

    return url

def get_fbm_search_results(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--log-level = 1")
    options.add_argument("permissions-policy: interest-cohort=()")
    browser = webdriver.Firefox(options=options)
    browser.get(url)
    html_source = browser.page_source
    browser.quit()

    soup = BeautifulSoup(html_source, 'html.parser')

    if not soup:
        return None

    listings = soup.find('div',class_='bq4bzpyk j83agx80 btwxx1t3 lhclo0ds jifvfom9 muag1w35 dlv3wnog enqfppq2 rl04r1d5').find_all('div')

    urls = []
    for i in listings:
        try:
            urls += ['https://www.facebook.com' + i.find('div').find('div').find('div').find('a')['href'].split('/?ref=search')[0]]
        except:
            pass

    return urls

def fbm_main(search_term, region='edmonton'):
    url_list = get_fbm_search_results(make_fbm_search_url(search_term))

    if not url_list:
        url_list = []

    object_list = []

    print("Found " + str(len(url_list)) + " listings on Facebook Marketplace. Search term : " + search_term + " Region : " + region)

    for url in tqdm(url_list):
        #time.sleep(0.5)
        attribute_dict = get_fbm_page_info(url)

        if attribute_dict:
            container = StorageBoi(pricE=attribute_dict['price'], urL=url, titlE=attribute_dict['title'], descriptioN=attribute_dict['content'], categorY=attribute_dict['category'], datE=attribute_dict['date'])
            object_list += [container]

    print("Done fetching results from Facebook Marketplace.")
    return object_list

if __name__ == "__main__":
    #url = "https://www.facebook.com/marketplace/item/205016458501904"
    #print(get_fbm_page_info(url))

    print(fbm_main('ryzen'))
