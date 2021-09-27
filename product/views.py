from django.db.models import Q
from django.views import generic

from product.models import Product, Category, PropertyDescription


class HomeView(generic.ListView):
    template_name = 'home/home.html'

    def get_queryset(self):
        all_categories = Category.objects.all()
        products = [
                {'name': category.name,
                 'products': Product.objects.filter(category__name=category.name)} for category in all_categories]
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductView(generic.DetailView):
    model = Product
    template_name = 'product/product.html'
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['object']
        category = context['object'].category.id
        context['other-products'] = Product.objects.filter(
            (Q(category__id=category) | Q(category__parent__id=category)) if category else
            (Q(category__name__contains=category) | Q(category__parent__name__contains=category))).exclude(id=product.id)
        return context
