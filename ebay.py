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


def get_ebay_page_info(url):
    page = requests.get(url)
    soup = get_page(url)
    
    if not soup:
        return None

    try:
        html = list(soup.children)[2]
        head = list(html.children)[1]
        body = list(html.children)[3]
    except:
        return None

    
    #finds title of listing
    try:
        title = head.find('title').get_text()
        title = title.replace("  | eBay","")  #strip eBay label
    except:
        title = None
    
    #finds cost depending on if listing is auction or not
    try:
        is_auction = 'bids' in list(body.find_all('div', class_='vi-flex-cta'))[0].get_text()
    except:
        is_auction = None
    
    if is_auction != None:
        try:   
            if is_auction:
                transaction_type = "AUCTION"
                #retreives cost for bid/auctioned listings
                cost = list(body.find_all('div', class_='val vi-price'))[0].find('span').get_text()
            elif not is_auction:
                transaction_type = "SELLING"
                #retrieves cost for non-bid/auctioned listings
                cost = list(body.find_all('div', class_='mainPrice'))[0].find('div').find('span').get_text()
            unit = "USD"
            cost = cost.replace("$","")   #strip details
            cost = cost.replace("US","")
        except:
            cost = None
            unit = None
            transaction_type = None
            
        #format cost to an output that fits storageBoi() function
        price = [cost, unit, transaction_type]  #assumes all prices are listed as USD     
        

    #find listing content (new, used, etc.)
    try:
        content_description = list(body.find_all('div', class_='nonActPanel'))[0].find('div').get_text()
        for i in ['\n','\t']:
            content_description = content_description.replace(i,"")  #strip formatting whitespace
    except:
        content_description = None
    
    #find category
    try:
        category = list(body.find_all('nav', class_='vi-bc-topM'))[0].get_text()
        category = category[category.rfind('>'):]
        for i in ['>','\n','Add to Watch list','|']:   #yikes
            category = category.replace(i,"")
    except:
        category = None
    

    return(price,url,title,content_description,category)



def make_ebay_search_url(search_string, region='edmonton', ):
    search_string = search_string.lower().replace(' ', '%20')

    #with eBay, no region necessary
    print('Searching in North America.')

    url = "https://www.ebay.ca/sch/i.html?_nkw=" + search_string 

    return url



def get_ebay_search_results(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    #html = list(soup.children)[2]
    #head = list(html.children)[1]
    #body = list(html.children)[3]

    return [i.find('a')['href'] for i in list(soup.find_all('div', class_='s-item__image'))]



