from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from user.api.views import (
    UserViewSet,
    CustomerUserViewSet,
    register_login_view,
    check_user_code,
    refresh_code,
    login_with_password,
    reset_password_get_code,
    check_code_for_reset_password,
    change_password
)

app_name = 'auth_api'

router = routers.DefaultRouter()

router.register(r'all', UserViewSet)
router.register(r'customers', CustomerUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register-login', register_login_view, name='register-login'),
    path('check-code', check_user_code, name='check-code'),
    path('login', obtain_auth_token, name='login'),
    path('refresh-code', refresh_code, name='refresh-code'),
    path('login-with-password', login_with_password, name='login-with-password'),
    path('reset-password-get-code', reset_password_get_code, name='reset-password-get-code'),
    path('check-code-reset-password', check_code_for_reset_password, name='check-code-reset-password'),
    path('change-password', change_password, name='change-password'),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
