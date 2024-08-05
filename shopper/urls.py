from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='shopper-home'),
    path('search/', views.search, name='search'),
    path('product_chart', views.product_chart, name='product_chart'),
    path('post/ajax/search', views.post_return_search, name='post_search'),
    path('post/ajax/save-prod-search', views.post_save_prod_search, name='post_save_prod_search')
]
