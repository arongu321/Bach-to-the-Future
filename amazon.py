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
    Debug = False
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--log-level = 1")
    options.add_argument("permissions-policy: interest-cohort=()")
    driver = webdriver.Firefox(options= options)
    request = driver.get("https://www.amazon.com/s?k="+search_key)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "s-result-item")))
    page_source = driver.page_source
    page = BeautifulSoup(page_source , "html.parser")
    if page !=  None:
        listings = get_page_content(page)
    else:
        if Debug:
            print("page is none")
        return None
        
    # Now we have to parse the listings according to search criteria(for future criteria)
    if listings != None:
        if Debug:
            print("in get_prod_objs")
        objs = get_prod_objects(listings)
    else:
        return None
    if Debug:
        print(objs)
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
    try:
        listings = page.findAll("div",attrs = {"class":"s-result-item"})[1:]
    except:
        return None
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
            except:
                continue
            try:
                price = product.find("span",attrs={"class":"a-offscreen"}).text.strip() 
                price = float(price[1:]) if float(price[1:]) else 0
                if Debug:
                    print(price,end="")
            except:
                price = None
                if price == None:
                    price = product.find("span",attrs = {"class":"a-price-whole"}).text.strip()
                    try:
                        price = float(price)
                    except:
                        try:
                            price = float(price[1:])
                            price = float(price[1:]) if float(price[1:]) else 0
                            if Debug:
                                print(price , end="")
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
            # From the link we need to get to the listing page  to get the description
            try:
                product_desc = requests.get("https://amazon.com"+link)
            except:
                continue
            if name != None and link!= None and price!= None :
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
                    
                    # We have the description and now just need to export the object using storageBoi
                storage_object = StorageBoi(pricE = [price, "CAD", "SELLING"] ,urL = "https://amazon.com/"+link , descriptioN= content , titlE = name , categorY = category, datE = None )
                object_list += [storage_object]    
            else:
                continue
        except:
            continue
    return object_list


if __name__ == "__main__":
    search_string = "rtx 3080 ti EVGA"
    obj_list = main_amazon(search_string)
    print(obj_list)
            