from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserLogin, UserCode


# Create your views here.
def user_register_login(request):
    form = UserLogin()
    context = {
        'phone': True,
        'form': form,
    }
    return render(request, 'customer/register-login.html', context=context)


def user_login(request):
    form = UserCode()
    context = {
        'code': True,
        'form': form,
        'login': True
    }
    return render(request, 'customer/register-login.html', context=context)


def user_register(request):
    form = UserCode()
    context = {
        'code': True,
        'form': form,
        'register': True
    }
    return render(request, 'customer/register-login.html', context=context)
