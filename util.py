import requests
from bs4 import BeautifulSoup
import time
from tkinter import *
import tkinter as tk
from tkinter import ttk

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

# from https://data-flair.training/blogs/currency-converter-python/
def convert(from_currency, to_currency='USD', amount=None):
    data = requests.get('https://api.exchangerate-api.com/v4/latest/USD').json()
    if amount == 0:
        return 0
    elif not amount:
        return None

    if type(amount) == str:
        try:
            amount.replace(',', '')
            amount = int(amount)
        except:
            amount = None

    currencies = data['rates']
    initial_amount = amount

    if from_currency == 'CAN':
        from_currency = 'CAD'

    try:
        if from_currency != 'USD':
            amount = amount / currencies[from_currency]

            # limiting the precision to 4 decimal places
        amount = round(amount * currencies[to_currency], 4)
        return amount

    except:
        return None
