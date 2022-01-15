import requests
from bs4 import BeautifulSoup
import csv
import os

def search_url(search_string):

    
    url = "https://www.amazon.com/s?k="+search_string
    page = requests.get(url,headers = headers)
    return page

def get_page_content(page):

    status = page.status_code

    if status == 200:

        soup = BeautifulSoup(page.content , "html.parser")
        #print(soup)
        listings = soup.findAll("div",attrs = {"class":"s-result-item"})[0:-2]

        return listings
       
    else:
        print(status)
        return False

if __name__ == "__main__":
    headers = {
        
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',

    }
    # for now the url is hardcoded with the string given by the main.py file
    search_string = "gtx 1660 "

    page = search_url(search_string)
    
    listings = get_page_content(page)

#   now we have to parse the listings according to search criteria(for future criteria)

    for product in listings:
            name = product.find("span",attrs={"class":"a-size-medium"})
            print(name.text)
            break

