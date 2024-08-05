import os
import re
import time
import json

import requests
from bs4 import BeautifulSoup

from .logger import write_file, write_logger

emag_category = ""
emag_list = {}
emag_list["products"] = []

def emag_price_converter(price_string, type):
    price_string = price_string.strip()
    arr = re.findall(r'\d+', price_string)
    if type == "new":
        pass
        if len(arr) == 1:
            return int(arr[0]) / 100
        elif len(arr) == 2:
            new_p = arr[0] + arr[1]
            return int(new_p) / 100
    elif type == "old":
        if len(arr) > 0:
            new_p = arr[0] + arr[1]
            return int(new_p) / 100


def filter_name(product, product_query):
    for word in product_query.split():
        if word.upper() not in product.upper():
            return False
    return True


def find_products_emag(soup, product_query):
    global emag_category, emag_list
    # find the product category based on first search result
    item_card = soup.find_all('div', {'class': 'js-product-data'})[0]

    if emag_category == "":
        emag_category = item_card['data-category-trail']
        print("Emag product category: " + emag_category)

    product_cards = soup.find_all('div', {'class': 'js-product-data'})
    for card in product_cards:
        write_logger(card.get_text())
        product_link_map = {}
        if card.has_attr('data-category-trail') and card.has_attr('data-name'):
            if card['data-category-trail'] == emag_category and filter_name(card['data-name'].upper(), product_query):
                product_link_map['retailer'] = 'emag'
                product_href = card.find('a', {'class': 'product-title'})
                product_link_map['link'] = product_href['href']
                product_link_map['name'] = product_href['title']
                product_new_price = card.find('p', {'class': 'product-new-price'})
                product_link_map['price'] = emag_price_converter(product_new_price.get_text(), "new")
                product_old_price = card.find('p', {'class': 'product-old_price'})
                if not (product_old_price is None):
                    if product_old_price.get_text() != "":
                        product_link_map['old_price'] = emag_price_converter(product_old_price.get_text(), "old")
                else:
                    product_link_map['old_price'] = product_link_map['price']
                product_link_map["date_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                emag_list["products"].append(product_link_map)


def scrape_emag(product_query):
    global emag_category, emag_list

    emag_category = ""
    emag_list = {}
    emag_list["products"] = []

    for i in range(1,3):
        search_page_link = "https://www.emag.ro/search/{}/p{}".format(product_query, str(i))
        req_search = requests.get(search_page_link)
        if req_search.status_code == 200:
            soup = BeautifulSoup(req_search.content, 'html.parser')
            find_products_emag(soup, product_query)
            print("Scrapped the info from search page: " + search_page_link)
            write_file(emag_list, "emag", product_query)
            time.sleep(2)
        else:
            print("Failed to get response from \'{}\'".format(search_page_link))
    return emag_list
