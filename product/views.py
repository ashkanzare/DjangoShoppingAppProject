from django.shortcuts import render

# Create your views here.
from django.views import generic

from product.models import Product


class HomeView(generic.ListView):
    template_name = 'home/home.html'
    queryset = Product.objects.all()
