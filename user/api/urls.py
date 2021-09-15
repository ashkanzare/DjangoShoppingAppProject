from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from user.api.views import UserViewSet, CustomerUserViewSet, register_login_view, check_user_code

router = routers.DefaultRouter()

router.register(r'all', UserViewSet)
router.register(r'customers', CustomerUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register-login', register_login_view, name='register-login'),
    path('check-code', check_user_code, name='check-code'),
    path('login', obtain_auth_token, name='login')
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
