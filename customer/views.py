from django.shortcuts import render
from django.views.generic import ListView
from rest_framework.authtoken.models import Token

from order.models import Order
from customer.forms import UserRegisterLogin, UserCode, UserPassword, ResetPassword
from customer.models import Customer, Address, MeCoinWallet


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
    auth_by = request.GET.get('by')
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
            'login_type': check_login_type,
            'auth_by': auth_by
        }
        return render(request, 'customer/register-login.html', context=context)
    except Token.DoesNotExist:
        return render(request, '404.html', context={})


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
        return render(request, '404.html', context={})


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
        return render(request, '404.html', context={})


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
        return render(request, '404.html', context={})


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
        return render(request, '404.html', context={})


class CustomerProfileListView(ListView):
    """
    view for see profile of a user
    """
    model = Customer
    template_name = 'customer/profile/customer_profile.html'
    context_object_name = 'customer_object'

    def get_queryset(self):
        logged_in_user = self.request.user
        return Customer.get_by_user_or_none(logged_in_user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_three_orders'] = Order.objects.filter(cart__customer=self.get_queryset())
        return context

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_anonymous:
            if self.get_queryset():
                return super(CustomerProfileListView, self).get(request, *args, **kwargs)
        return render(request, '404.html', context={})


class CustomerProfileEditListView(ListView):
    """
    view for edit profile of a user
    """
    model = Customer
    template_name = 'customer/profile/edit-profile.html'
    context_object_name = 'customer_object'

    def get_queryset(self):
        logged_in_user = self.request.user
        return Customer.get_by_user_or_none(logged_in_user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['token'] = Token.objects.get(user=self.request.user).key
        context['days'] = [i for i in range(1, 32)]
        context['months'] = [i for i in range(1, 13)]
        context['years'] = [i for i in range(1310, 1384)]
        return context

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_anonymous:
            if self.get_queryset():
                return super(CustomerProfileEditListView, self).get(request, *args, **kwargs)
        return render(request, '404.html', context={})


class CustomerAddressListView(ListView):
    """
    view for see addresses of a user
    """
    model = Customer
    template_name = 'customer/address/customer-address.html'
    context_object_name = 'customer_object'

    def get_queryset(self):
        logged_in_user = self.request.user
        return Customer.get_by_user_or_none(logged_in_user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = Address.objects.filter(customer__user=self.request.user)
        return context

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_anonymous:
            if self.get_queryset():
                return super(CustomerAddressListView, self).get(request, *args, **kwargs)
        return render(request, '404.html', context={})


class CustomerWalletListView(ListView):
    """
    view for see wallet of a user
    """
    model = Customer
    template_name = 'customer/profile/wallet.html'
    context_object_name = 'customer_object'

    def get_queryset(self):
        logged_in_user = self.request.user
        return MeCoinWallet.objects.get(customer__user=logged_in_user)

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_anonymous:
            if self.get_queryset():
                return super(CustomerWalletListView, self).get(request, *args, **kwargs)
        return render(request, '404.html', context={})
