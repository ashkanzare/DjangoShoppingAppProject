from django.shortcuts import render
from django.views import generic
from rest_framework.authtoken.models import Token

from product.models import Product
from .forms import UserLogin, UserCode


# Create your views here.
def user_register_login(request):
    """
    check if user is registered before or not and redirect to proper url (with ajax)

    """
    form = UserLogin()
    context = {
        'phone': True,
        'form': form,
    }
    return render(request, 'customer/register-login.html', context=context)


def user_login(request, token):
    """
        view for login a user

    """
    token = request.GET.get('token')
    try:
        Token.objects.get(key=token)
        form = UserCode()
        context = {
            'code': True,
            'form': form,
            'login': True
        }
        return render(request, 'customer/register-login.html', context=context)
    except Token.DoesNotExist:
        return render(request, 'page_not_found/page_not_found.html', context={})


def user_register(request, token):
    """
    view for register a user

    """
    token = request.GET.get('token')
    try:
        Token.objects.get(key=token)
        form = UserCode()
        context = {
            'code': True,
            'form': form,
            'register': True
        }
        return render(request, 'customer/register-login.html', context=context)
    except Token.DoesNotExist:
        return render(request, 'page_not_found/page_not_found.html', context={})


class HomeView(generic.ListView):
    template_name = 'home/home.html'
    queryset = Product.objects.all()
