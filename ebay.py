import requests
from bs4 import BeautifulSoup
import time
from storageBoi import StorageBoi
from util import get_page
from tqdm import tqdm


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
                if cost == 'Discounted price':   # handle discounted prices
                    cost = list(body.find_all('div', class_='mainPrice'))[0].find('div').find('span',class_='notranslate').get_text()
                    
            if "US" in cost:
                unit = "USD"
                cost = cost.replace("US ","")
            elif "C" in cost:
                unit = "CAN"
                cost = cost.replace("C ","")                
            cost = float(cost.replace("$","").replace(",",""))   #strip details
                
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
    

    return{'price':price, 'title':title, 'category':category, 'content':content_description}




def make_ebay_search_url(search_string, region='edmonton', ):
    search_string = search_string.lower().replace(' ', '%20')

    #with eBay, no region necessary
    print('Searching Internationally.')

    url = "https://www.ebay.ca/sch/i.html?_nkw=" + search_string 

    return url



def get_ebay_search_results(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    #html = list(soup.children)[2]
    #head = list(html.children)[1]
    #body = list(html.children)[3]

    items = [i.find('a')['href'] for i in list(soup.find_all('div', class_='s-item__image'))]
    
    for i in range(0,len(items)):
        items[i] = items[i][0:36]
        
    return items



def ebay_main(search_term, region='edmonton'):
    url_list = get_ebay_search_results(make_ebay_search_url(search_term))

    object_list = []

    print("Found " + str(len(url_list)) + " listings on ebay. Search term : " + search_term + " Region : " + 'n/a')

    for url in tqdm(url_list):
        time.sleep(0.5)
        attribute_dict = get_ebay_page_info(url)

        if attribute_dict:
            container = StorageBoi(pricE=attribute_dict['price'], urL=url, titlE=attribute_dict['title'], descriptioN=attribute_dict['content'], categorY=attribute_dict['category'])
            object_list += [container]

    print("Done fetching results from ebay.")
    return object_list
