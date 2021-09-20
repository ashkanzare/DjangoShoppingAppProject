from django.urls import path

from product.views import HomeView

app_name = 'product'

urlpatterns = [
    # home url
    path('', HomeView.as_view(), name='home')

]
