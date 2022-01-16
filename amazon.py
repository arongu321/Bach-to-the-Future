from distutils.log import error
from msilib.schema import Error
from re import search
import requests
from bs4 import BeautifulSoup
import csv
import os
import sys
    

def main_amazon(search_string):
   
    # for now the url is hardcoded with the string given by the main.py file
    

    s = requests.Session()
    url = "https://www.amazon.com/s?k="+search_string
    try:
        page = s.get(url,headers = headers)
    except:
        print("the url didn't work :(")
        url = None

    listings = get_page_content(page)

#   now we have to parse the listings according to search criteria(for future criteria)
    objs = get_prod_objects(listings,s)





def get_page_content(page):

    status = page.status_code

    if status == 200:
        
        soup = BeautifulSoup(page.content , "html.parser")
       
        try:
            listings = soup.findAll("div",attrs = {"class":"s-result-item"})[0:-2]
        except:
            return None

        return listings
       
    else:
        
        print("error in get_page_content",status)
        return None
  
def get_prod_objects(listings,session):
    try:
        for product in listings[:2]:
            try:
                name = product.find("span",attrs={"class":"a-size-medium"}).text.strip()
                #search_list = search_string.split()
                """
                for term in search_list:
                    if term  in name.split():
                        cflag = True
                 
                    
                if cflag:
                    print(name)
                else:
                    return None
                """
            except:
                name = None

            try:
                price = product.find("span",attrs={"class":"a-offscreen"}).text.strip()
                print(price)
            except:
                price = None

            try:
                link = product.find("a",attrs={"class":"a-link-normal s-link-style a-text-normal"})["href"].strip()
                print(link)
            except:
                link = None
            #from the link we need to get to the listing page  to get the description

            
            product_desc = session.get("https://amazon.com"+link,headers = headers)
            if product_desc.status_code == 200:
                    soup_desc = BeautifulSoup(product_desc.content, "html.parser")
                    try:                    
                        description = soup_desc.find("div",attrs={"data-feature-name":"productDescription"})
                    
                        description = description.find("div",attrs={"id":"productDescription"}).find("span").text.strip()
                    except:
                        description = soup_desc.findAll("table",attrs={"class":"a-bordered a-horizontal-stripes aplus-tech-spec-table"})
                        content = ""
                        for element in description:
                            for i in element.findAll("td"):
                                content += i.find("span").text.strip()
                        print(content)
                        # we have the description and now just need to export the object using storageBoi
                        

            else:
                    print(product_desc.status_code)
                    return None
            
    except:
        print("error in get_prod_objects")
        print(sys.stderr())
        print(len(listings))
        return None
    return 0

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
    search_string = "gtx 1650"
    main_amazon(search_string)
    """
            product urls:

            https://www.amazon.com/ZOTAC-GTX-1660-Graphics-ZT-T16620F-10L/dp/B07Z8PWC6R/ref=sr_1_1_mod_primary_new?crid=12JRZRLRPEXW0&keywords=gtx%2B1660&qid=1642284515&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sprefix=gtx%2B1660%2Caps%2C159&sr=8-1&th=1

            https://www.amazon.com/AMD-Ryzen-5900X-24-Thread-Processor/dp/B08164VTWH/ref=sr_1_1?crid=HCLAT56NH40N&keywords=amd&qid=1642286693&sprefix=amd%2Caps%2C141&sr=8-1
            https://www.amazon.com/AMD-Ryzen-5600X-12-Thread-Processor/dp/B08166SLDF/ref=pd_sbs_1/137-1421435-6885034?pd_rd_w=HfJy4&pf_rd_p=3676f086-9496-4fd7-8490-77cf7f43f846&pf_rd_r=7R7QFEQG7HW2TYDFDTTH&pd_rd_r=2a55cf70-3045-443a-bced-35eafb738489&pd_rd_wg=zP90J&pd_rd_i=B08166SLDF&psc=1

    """
            

