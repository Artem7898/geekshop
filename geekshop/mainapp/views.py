import datetime
import json
import os
import random

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.context_processors import basket
from mainapp.models import ProductCategory, Product



def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return []

def get_hot_product():
    products = Product.objects.all()

    return random.sample(list(products), 1)[0]

def get_same_products(hot_product):
    return Product.objects.filter(category__pk=hot_product.category.pk).exclude(pk=hot_product.pk)[:3]


def main(request):
    title = 'главная'
    products = Product.objects.all()[:0]

    content = {'title': title, 'products': products,}
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None, page=1):
    title = 'продукты'
    links_menu = ProductCategory.objects.all()

    if pk is not None:
        if pk:
            if pk == '0':
                products = Product.objects.all().order_by('price')
                category = {'name': 'все','pk':0}
            else:
                category = get_object_or_404(ProductCategory, pk=pk)
                products = Product.objects.filter(category__pk=pk).order_by('price')

            paginator = Paginator(products, 2)
            try:
                product_paginator = paginator.page(page)
            except PageNotAnInteger:
                product_paginator = paginator.page(1)
            except EmptyPage:
                product_paginator = paginator.page(paginator.num_pages)


            content = {
                'title': title,
                'links_menu': links_menu,
                'category': category,
                'products': product_paginator,

            }

            return render(request, 'mainapp/products_list.html', content)


    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)


    content = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
        'basket': basket(request.user),
        'hot_product': hot_product,
    }

    return render(request, 'mainapp/products.html', content)


def product(request, pk):
    title = 'продукты'

    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),

    }

    return render(request, 'mainapp/product.html', content)


def contact(request):
    title = 'о нас'
    visit_date = datetime.datetime.now()
    locations = [
        {
            'city': 'Москва',
            'phone': '+7-888-888-8888',
            'email': 'info@geekshop.ru',
            'address': 'В пределах МКАД',
        },
        {
            'city': 'Екатеринбург',
            'phone': '+7-777-777-7777',
            'email': 'info_yekaterinburg@geekshop.ru',
            'address': 'Близко к центру',
        },
        {
            'city': 'Владивосток',
            'phone': '+7-999-999-9999',
            'email': 'info_vladivostok@geekshop.ru',
            'address': 'Близко к океану',
        },
    ]
    content = {'title': title, 'visit_date': visit_date, 'locations': locations}
    return render(request, 'mainapp/contact.html', content)


def contact(request):
    title = 'о нас'
    visit_date = datetime.datetime.now()
    locations = []
    file_path = os.path.join(settings.BASE_DIR, 'contacts.json')
    with open(file_path) as file_contacts:
        # file_content = file_contacts.read()
        locations = json.load(file_contacts)
    content = {'title': title, 'visit_date': visit_date, 'locations': locations}
    return render(request, 'mainapp/contact.html', content)
