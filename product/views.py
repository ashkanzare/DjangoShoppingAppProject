from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.views import generic

from product.models import Product, Category


class HomeView(generic.ListView):
    template_name = 'home/home.html'

    def get_queryset(self):
        all_categories = Category.objects.all()
        products = [
            {'name': category.name,
             'products': Product.objects.filter(category__name=category.name)} for category in
            all_categories]
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
        context['other_products'] = Product.objects.filter(
            (Q(category__id=category) | Q(category__parent__id=category)) if category else
            (Q(category__name__contains=category) | Q(category__parent__name__contains=category))).exclude(
            id=product.id)

        all_products = Product.objects.filter(
            (Q(category__id=category) | Q(category__parent__id=category)) if category else
            (Q(category__name__contains=category) | Q(category__parent__name__contains=category))).exclude(
            id=product.id)
        page = self.request.GET.get('page', 1)
        paginator = Paginator(all_products, 1)
        try:
            context['other_products'] = paginator.page(page)
        except PageNotAnInteger:
            context['other_products'] = paginator.page(1)
        except EmptyPage:
            context['other_products'] = paginator.page(paginator.num_pages)

        return context
