from django.views import generic

from product.models import Product, Category


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

