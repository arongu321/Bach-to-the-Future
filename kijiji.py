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


url = 'https://www.kijiji.ca/v-monitors/edmonton/monitor-arm-dual-monitor-arm/1601268382?cid=e507e4e1-63d8-4af4-b337-63a18f4c6c07'

for i in get_kijiji_page_info(url):
    print(i)