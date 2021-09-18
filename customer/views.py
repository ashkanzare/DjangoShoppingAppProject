from django.shortcuts import render
from django.views import generic
from rest_framework.authtoken.models import Token

from product.models import Product
from .forms import UserRegisterLogin, UserCode, UserPassword, ResetPassword


# Create your views here.
def user_register_login(request):
    """
    check if user is registered before or not and redirect to proper url (with ajax)

    """
    form = UserRegisterLogin()
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
    check_login_type = request.GET.get('login_type')
    try:
        check_token = Token.objects.get(key=token)

        if check_login_type == 'password':
            form = UserPassword()
        else:
            form = UserCode()

        context = {
            'code': True,
            'form': form,
            'login': True,
            'phone_number': check_token.user.phone,
            'token': token,
            'login_type': check_login_type
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
        check_token = Token.objects.get(key=token)
        form = UserCode()
        context = {
            'code': True,
            'form': form,
            'register': True,
            'phone_number': check_token.user.phone
        }
        return render(request, 'customer/register-login.html', context=context)
    except Token.DoesNotExist:
        return render(request, 'page_not_found/page_not_found.html', context={})


def phone_reset_password(request, token):
    """
    view for reset password for a user

    """
    token = request.GET.get('token')
    try:
        Token.objects.get(key=token)
        form = UserRegisterLogin()
        context = {
            'form': form,
            'phone': True,
        }
        return render(request, 'customer/auth/restore-password.html', context=context)
    except Token.DoesNotExist:
        return render(request, 'page_not_found/page_not_found.html', context={})


def confirm_code_for_reset_password(request, token):
    """
    view for confirm code for reset password for a user

    """
    token = request.GET.get('token')
    try:
        check_token = Token.objects.get(key=token)
        form = UserCode()
        context = {
            'code': True,
            'form': form,
            'register': True,
            'phone_number': check_token.user.phone
        }
        return render(request, 'customer/auth/restore-password.html', context=context)
    except Token.DoesNotExist:
        return render(request, 'page_not_found/page_not_found.html', context={})


def reset_password(request, token):
    """
    view for reset password

    """

    token = request.GET.get('token')
    try:
        check_token = Token.objects.get(key=token)
        user = check_token.user
        form = ResetPassword()
        context = {
            'reset': True,
            'form': form,
            'token': token
        }

        return render(request, 'customer/auth/restore-password.html', context=context)
    except Token.DoesNotExist:
        return render(request, 'page_not_found/page_not_found.html', context={})


class HomeView(generic.ListView):
    template_name = 'home/home.html'
    queryset = Product.objects.all()
