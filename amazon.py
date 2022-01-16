import requests
from bs4 import BeautifulSoup , SoupStrainer
import csv
import os
import sys
from storageBoi import StorageBoi
from tqdm import tqdm
import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def main_amazon(search_key):
    
    global Debug
    Debug = True
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--log-level = 1")
    options.add_argument("permissions-policy: interest-cohort=()")
    #driver = webdriver.Firefox(executable_path="C:\\Users\\bachw\\Documents\\GitHub\\Bach-to-the-Future\\geckodriver",options= options)
    driver = webdriver.Firefox(options= options)
    request = driver.get("https://www.amazon.com/s?k="+search_key)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "s-result-item")))
    page_source = driver.page_source

    page = BeautifulSoup(page_source , "html.parser")
    
    
    if page !=  None:
            
            listings = get_page_content(page)
    else:
            if Debug :
                print("page is none")
            return None
    #   now we have to parse the listings according to search criteria(for future criteria)
    if listings != None:
            if Debug:
                print("in get_prod_objs")
            objs = get_prod_objects(listings)
    else:
        return None
    if Debug:
        print(objs)
    #driver.close()
    return objs

def GET_UA():
    uastrings = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",\
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",\
                    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",\
                    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",\
                    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"\
                    ]
    
    return random.choice(uastrings)

def get_page_content(page):
    
        #print(type(page),len(page))
        #soup = BeautifulSoup(page , "html.parser")
        
        #print(soup)
        try:
            listings = page.findAll("div",attrs = {"class":"s-result-item"})[1:]
            
        except:
            return None
        #print(listings)
        return listings
    
    
        
    
    
def get_prod_objects(listings):
            object_list = []
            print("Amazon scraper , Number of listings  " + str(len(listings)) + " :")
            

            for product in tqdm(listings):
                time.sleep(0.2)
                try:
                    
                    try:
                        
                        name = product.find("span",attrs={"class":"a-size-medium"}).text.strip()
                        if Debug:
                            print(name,end="")
                        """
                        search_list = search_string.split()
                        
                        for term in search_list:
                            if term  in name.split():
                                cflag = True
                        
                            
                        if cflag:
                            pass
                        else:
                            continue
                        
                    """    
                    except:
                        continue
                    
                    try:
                        price = product.find("span",attrs={"class":"a-offscreen"}).text.strip()
                        
                        price = [float(price[1:]) if float(price[1:]) else 0, "CAD", "SELLING"]
                        if Debug:
                            print(price,end="")
                    except:
                        #print(price)
                        if price == None:
                           
                            price = product.find("span",attrs = {"class":"a-price-whole"}).text.strip()
                            try:
                                price = float(price)
                            except:
                                try:
                                    price = float(price[1:])
                                    price = [float(price[1:]) if float(price[1:]) else 0, "CAD", "SELLING"]
                                    if Debug:
                                        print(price , ends="")
                                except:
                                    pass
                                pass

                    try:
                        link = product.find("a",attrs={"class":"a-link-normal s-link-style a-text-normal"})["href"].strip()
                        if Debug:
                            print(link,end="")
                        if "redirect" in link:
                            continue
                    except:
                        link = None

                    try:
                        category = product.find("a",attrs={"class":"a-list-item"}).text.strip()
                    except:
                        category = None
                    #from the link we need to get to the listing page  to get the description

                    try:

                        product_desc = requests.get("https://amazon.com"+link)
                    except:
                        continue
                    if name != None and link!= None and price!= None :
                            #print("in prod desc")
                            #soup_desc = BeautifulSoup(product_desc.content, "html.parser" )
                            try:  
                                strainer = SoupStrainer("div")
                                soup_desc = BeautifulSoup(product_desc.content, "lxml" , parse_only = strainer)                  
                                description = soup_desc.find("div",attrs={"data-feature-name":"productDescription"})
                            
                                content = description.find("div",attrs={"id":"productDescription"}).find("span").text.strip()
                                
                            except:
                                strainer = SoupStrainer("table")
                                soup_desc = BeautifulSoup(product_desc.content, "lxml" , parse_only = strainer)                  
                                description = soup_desc.findAll("table",attrs={"class":"a-bordered a-horizontal-stripes aplus-tech-spec-table"})
                                content = ""
                                for element in description:
                                    for i in element.findAll("td"):
                                        content += i.find("span").text.strip()
                                
                                # we have the description and now just need to export the object using storageBoi
                            storage_object = StorageBoi(pricE = price ,urL = link , descriptioN= content , titlE = name , categorY = category, datE = None )
                            #print("price :", price , "title :", name)
                            object_list += [storage_object]
                            
                    else:
                            #print(product_desc.status_code)
                            continue
                except:
                    continue
            
            return object_list


if __name__ == "__main__":
        
        search_string = "rtx 3080 ti EVGA"
        obj_list = main_amazon(search_string)
        print(obj_list)
        """
                product urls:

                https://www.amazon.com/ZOTAC-GTX-1660-Graphics-ZT-T16620F-10L/dp/B07Z8PWC6R/ref=sr_1_1_mod_primary_new?crid=12JRZRLRPEXW0&keywords=gtx%2B1660&qid=1642284515&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sprefix=gtx%2B1660%2Caps%2C159&sr=8-1&th=1

                https://www.amazon.com/AMD-Ryzen-5900X-24-Thread-Processor/dp/B08164VTWH/ref=sr_1_1?crid=HCLAT56NH40N&keywords=amd&qid=1642286693&sprefix=amd%2Caps%2C141&sr=8-1
                https://www.amazon.com/AMD-Ryzen-5600X-12-Thread-Processor/dp/B08166SLDF/ref=pd_sbs_1/137-1421435-6885034?pd_rd_w=HfJy4&pf_rd_p=3676f086-9496-4fd7-8490-77cf7f43f846&pf_rd_r=7R7QFEQG7HW2TYDFDTTH&pd_rd_r=2a55cf70-3045-443a-bced-35eafb738489&pd_rd_wg=zP90J&pd_rd_i=B08166SLDF&psc=1

        """
            