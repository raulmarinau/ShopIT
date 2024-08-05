from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

from .forms import SearchForm
from .models import Saved_Product, Saved_Product_Info, CustomUser_NestedField
from .documents import Saved_Product_Document

from scrapyboi import find_product


def home(request):
    return render(request, 'shopper/home.html')


@login_required
def search(request):
    form = SearchForm()
    return render(request, 'shopper/search.html', {'form': form})


def post_return_search(request):
    if request.is_ajax and request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            prod_query = form.cleaned_data.get('search_term')
            products = find_product.scrapeIT(prod_query, request.user)
            for prod_list in products['products']:
                product = Saved_Product_Document.search().query("match", name = prod_list['link'])[:1]
                queryset_product = product.to_queryset()
                if len(queryset_product) == 0:
                    prod = Saved_Product(
                        name = prod_list['name'],
                        link = prod_list['link'],
                        retailer = prod_list['retailer']
                    )
                    prod_info = Saved_Product_Info(
                        price = prod_list['price'],
                        old_price = prod_list['old_price'],
                        product_base = prod
                    )
                    prod.save()
                    prod_info.save()
                else:
                    matched_prod = queryset_product[0]
                    if(prod_list['retailer'] == 'emag'):
                        if(matched_prod.name != prod_list['name']):
                            prod = Saved_Product(
                                name = prod_list['name'],
                                link = prod_list['link'],
                                retailer = prod_list['retailer']
                            )
                            prod_info = Saved_Product_Info(
                                price = prod_list['price'],
                                old_price = prod_list['old_price'],
                                product_base = prod
                            )
                            prod.save()
                            prod_info.save()
                        else:
                            prod_info = Saved_Product_Info(
                                price = prod_list['price'],
                                old_price = prod_list['old_price'],
                                product_base = matched_prod
                            )
                            prod_info.save()
                    elif(matched_prod.link != prod_list['link']):
                        prod = Saved_Product(
                            name = prod_list['name'],
                            link = prod_list['link'],
                            retailer = prod_list['retailer']
                        )
                        prod_info = Saved_Product_Info(
                            price = prod_list['price'],
                            old_price = prod_list['old_price'],
                            product_base = prod
                        )
                        prod.save()
                        prod_info.save()
                    else:
                            prod_info = Saved_Product_Info(
                                price = prod_list['price'],
                                old_price = prod_list['old_price'],
                                product_base = matched_prod
                            )
                            prod_info.save()
        return JsonResponse(products)


def post_save_prod_search(request):
    if request.is_ajax and request.method == "POST":
        if request.user.is_authenticated:
            product = Saved_Product_Document.search().query("match", name = request.POST.get("product[name]"))[:1]
            queryset_product = product.to_queryset()
            matched_prod = queryset_product[0]
            new_user = CustomUser_NestedField(
                user = request.user.username,
                product_base = matched_prod
            )
            new_user.save()
            return JsonResponse({})


def product_chart(request):
    prod_name = request.GET.get('prod_name')
    client = Elasticsearch()
    user_saved_products = Search(using=client).index("saved_products").query("match", name=prod_name)
    response = user_saved_products.execute()
    prod_infos = response.hits[0].infos
    prod_name = response.hits[0].name
    prod_link = response.hits[0].link
    return render(request, 'shopper/price_history.html', {'prod_infos': prod_infos, 'prod_name': prod_name, 'prod_link':prod_link})
