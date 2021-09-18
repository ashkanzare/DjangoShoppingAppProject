from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from .views import (
    user_register_login,
    user_login,
    user_register,
    confirm_code_for_reset_password,
    phone_reset_password,
    reset_password,
    CustomerProfileListView
)

app_name = 'customer'

urlpatterns = [
    path('register-login/', user_register_login, name="register-login"),
    path('login/<str:token>', user_login, name="login"),
    path('register/<str:token>', user_register, name="register"),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('customer:register-login')), name='logout'),
    path('confirm-code-reset-password/<str:token>', confirm_code_for_reset_password, name="confirm-code-reset-password"),
    path('phone-reset-password/<str:token>', phone_reset_password, name="phone-reset-password"),
    path('reset-password/<str:token>', reset_password, name="reset-password"),
    path('profile', CustomerProfileListView.as_view(), name="profile"),
    # path('courses-api/<str:text>', CourseViewSet.as_view(), name='courses-api')
]
