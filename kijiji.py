import requests
from bs4 import BeautifulSoup

def get_kijiji_page_info(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    html = list(soup.children)[2]
    head = list(html.children)[1]
    body = list(html.children)[3]

    price = list(body.find_all('div', class_='priceContainer-1419890179'))[0].find('span').find('span').get_text()
    title = head.find('title').get_text()
    content = list(body.find_all('div', class_='descriptionContainer-231909819'))[0].find('div').get_text()

    print(body)
    return(price, title, content)

def make_kijiji_search_url(search_string, region = 'edmonton', ):
    search_string = search_string.lower().replace(' ', '-')

    region_dict = {'edmonton' : 'k0c10l1700203',
                   'calgary' : 'k0c10l1700199'}

    url = "https://www.kijiji.ca/b-buy-sell/" + region + "/" + search_string + "/" + region_dict[region] + "?sort=dateAsc&dc=true"

    return url

def get_kijiji_search_results(url):
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    html = list(soup.children)[2]
    head = list(html.children)[1]
    body = list(html.children)[3]

    return ("https://www.kijiji.ca/" + i.find('a')['href'] for i in list(body.find_all('div', class_='title')))


[print(i) for i in get_kijiji_search_results(make_kijiji_search_url('AMD RYZEN', region='edmonton'))]

#url = 'https://www.kijiji.ca/v-monitors/edmonton/monitor-arm-dual-monitor-arm/1601268382?cid=e507e4e1-63d8-4af4-b337-63a18f4c6c07'

#for i in get_kijiji_page_info(url):
#    print(i)