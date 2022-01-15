import requests
from bs4 import BeautifulSoup

def get_kijiji_page_info(url):
    page = requests.get(url)

    #print(page.content)
    soup = BeautifulSoup(page.content, 'html.parser')
    #print(soup.prettify())

    html = list(soup.children)[2]

    head = list(html.children)[1]

    body = list(html.children)[3]

    price = list(body.find_all('div', class_='priceContainer-1419890179'))[0].find('span').find('span').get_text()
    return(price)


url = 'https://www.kijiji.ca/v-monitors/edmonton/monitor-arm-dual-monitor-arm/1601268382?cid=e507e4e1-63d8-4af4-b337-63a18f4c6c07'

print(get_kijiji_page_info(url))