import os
import re
import time
import json

import requests
from bs4 import BeautifulSoup

from .logger import write_file, write_logger

altex_list = {}
altex_list["products"] = []

def filter_name(product, product_query):
    for word in product_query.split():
        if word.upper() not in product.upper():
            return False
    return True


def filter_altex_json(json_arr, product_query):
    for data in json_arr:
        if filter_name(data['name'], product_query):
            altex_product = {}
            altex_product['retailer'] = 'altex'
            if 'name' in data:
                altex_product["name"] = data["name"]
            if 'price' in data:
                altex_product["price"] = data["price"]
            if 'regular_price' in data:
                altex_product["old_price"] = data["regular_price"]
            if 'url_key' in data:
                altex_product["link"] = "https://altex.ro/" + data["url_key"]
            altex_product["date_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            altex_list["products"].append(altex_product)


def scrape_altex(product_query):
    global altex_list

    altex_list = {}
    altex_list["products"] = []

    search_page_link = 'https://fenrir.altex.ro/catalog/search/{}'.format(product_query)
    req = requests.get(search_page_link)
    if req.status_code == 200:
        filter_altex_json(req.json()["products"], product_query)
        write_file(altex_list, "altex", product_query)
        print("Succesful request from altex: {}".format(search_page_link))
    else:
        print("Failed to get response from altex {}".format(search_page_link))
    return altex_list
