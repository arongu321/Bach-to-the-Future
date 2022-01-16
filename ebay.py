import requests
from bs4 import BeautifulSoup

def get_ebay_page_info(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    html = list(soup.children)[2]
    head = list(html.children)[1]
    body = list(html.children)[3]

    
    #finds title of listing
    title = head.find('title').get_text()
    title = title.replace("  | eBay","")  #strip eBay label
    
    #finds cost depending on if listing is auction or not
    is_auction = 'bids' in list(body.find_all('div', class_='vi-flex-cta'))[0].get_text()    
    if is_auction:
        transaction_type = "AUCTION"
        #retreives cost for bid/auctioned listings
        cost = list(body.find_all('div', class_='val vi-price'))[0].find('span').get_text()
    else:
        transaction_type = "SELLING"
        #retrieves cost for non-bid/auctioned listings
        cost = list(body.find_all('div', class_='mainPrice'))[0].find('div').find('span').get_text()
    cost = cost.replace("$","")   #strip details
    cost = cost.replace("US","")
    
    #format cost to an output that fits main() function
    price = [cost, "USD", transaction_type]  #assumes all prices are listed as USD     

    #find listing content (new, used, etc.)
    content_description = list(body.find_all('div', class_='nonActPanel'))[0].find('div').get_text()
    for i in ['\n','\t']:
        content_description = content_description.replace(i,"")  #strip formatting whitespace
    
    #find category
    category = list(body.find_all('nav', class_='vi-bc-topM'))[0].get_text()
    category = category[category.rfind('>'):]
    for i in ['>','\n','Add to Watch list','|']:   #yikes
        category = category.replace(i,"")
    
    
    return(price,url,title,content_description,category)


#auctioned example
#url ='https://www.ebay.ca/itm/144367449821?hash=item219cf876dd:g:TlcAAOSwO~Jh25v9'

#non-auctioned example
url = 'https://www.ebay.ca/itm/144273803417?hash=item2197638899:g:ww4AAOSwRZphgcUM'


print(get_ebay_page_info(url))
