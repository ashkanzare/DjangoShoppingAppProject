from django.urls import path, include
from rest_framework import routers

from user.api.views import UserViewSet, CustomerUserViewSet

router = routers.DefaultRouter()

router.register(r'all', UserViewSet)
router.register(r'customers', CustomerUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
