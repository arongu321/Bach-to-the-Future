import requests
from bs4 import BeautifulSoup
import time
from storageBoi import StorageBoi
from util import get_page

def get_kijiji_page_info(url):
    category = url[22:].split('/')[0]
    soup = get_page(url)

    if not soup:
        return None

    try:
        html = list(soup.children)[2]
        head = list(html.children)[1]
        body = list(html.children)[3]
    except:
        return None

    try:
        price = list(body.find_all('div', class_='priceContainer-1419890179'))[0].find('span').find('span').get_text()
    except:
        price = None
    try:
        currency = list(body.find_all('div', class_='priceContainer-1419890179'))[0].find('span').find_all('span')[1]['content']
    except:
        currency = None
    try:
        title = head.find('title').get_text().split('|')[0]
    except:
        title = None
    try:
        content = list(body.find_all('div', class_='descriptionContainer-231909819'))[0].find('div').get_text()
    except:
        content = None
    #try:
    #    print(list(body.find_all('script', type_='text/javascript')))
    #except:
    #    wanted = False

    if price == 'Free' or (price == None and category == "v-free-stuff"):
        price = 0
        listing_type = 'FREE'
    elif price.lower() == '':
        pass

    if price == 0:
        currency = 'CAD'

    if price == 'Please Contact':
        listing_type = 'CONTACT'
        price = None
        currency = 'CAD'
    else:
        listing_type = 'SELLING'

    price = float(price[1:])
    return{'price': [price, currency, listing_type], 'title': title, 'category': category, 'content': content}


def make_kijiji_search_url(search_string, region='edmonton', ):
    search_string = search_string.lower().replace(' ', '-')

    region = region.lower()

    region_dict = {'edmonton': 'k0c10l1700203',
                   'calgary': 'k0c10l1700199',
                   ''
                   'alberta': 'k0c10l9003',
                   'canada': 'k0l0',

                   }

    if region not in region_dict.keys():
        print('Unsupported region, searching all of Canada.')
        region = 'canada'

    url = "https://www.kijiji.ca/b-buy-sell/" + region + "/" + search_string + "/" + region_dict[region] + "?sort=dateAsc&dc=true"

    return url

def get_kijiji_search_results(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    html = list(soup.children)[2]
    head = list(html.children)[1]
    body = list(html.children)[3]

    return ["https://www.kijiji.ca" + i.find('a')['href'] for i in list(body.find_all('div', class_='title'))]

def kijiji_main(search_term, region='edmonton'):
    url_list = get_kijiji_search_results(make_kijiji_search_url(search_term))

    object_list = []

    print("Found " + str(len(url_list)) + " listings on Kijiji. Search term : " + search_term + " Region : " + region)

    for url in url_list:
        time.sleep(0.5)
        attribute_dict = get_kijiji_page_info(url)

        if attribute_dict:
            container = StorageBoi(pricE=attribute_dict['price'], urL=url, titlE=attribute_dict['title'], descriptioN=attribute_dict['content'], categorY=attribute_dict['category'])
            object_list += [container]

    print("Done fetching results from Kijiji.")
    return object_list

if __name__ == "__main__":
    pass
    #url_list = get_kijiji_search_results(make_kijiji_search_url('amd'))

    print(get_kijiji_page_info('https://www.kijiji.ca/v-desktop-computers/city-of-toronto/looking-for-i5-below-8-9th-gen-intel-cpu/1594701386'))
    #print(get_kijiji_page_info('https://www.kijiji.ca/v-baby-clothes-9-12-months/edmonton/looking-for-free-baby-clothing-and-blankets-only/1594926129'))


