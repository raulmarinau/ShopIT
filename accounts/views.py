from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

from .forms import UserRegisterForm
from shopper.models import Saved_Product, Saved_Product_Info, CustomUser_NestedField
from shopper.documents import Saved_Product_Document


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username} created succesfully!')
            return redirect('shopper-home')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    client = Elasticsearch()
    user_saved_products = Search(using=client).index("saved_products").query("nested", path="users", query=Q("term", **{'users.user': request.user.username}))
    user_saved_products.execute()
    return render(request, 'accounts/profile.html', {'user_saved_products': user_saved_products})
