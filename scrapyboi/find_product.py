from scrapyboi.crawlers import emag, altex
from django.contrib.auth.models import User


def scrapeIT(product_query, user):
    products = {}
    products = emag.scrape_emag(product_query)
    altex_prod = altex.scrape_altex(product_query) 
    products['products'].extend(altex_prod['products'])
    return products
