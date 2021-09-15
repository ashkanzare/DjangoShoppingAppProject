from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from .views import user_register_login, user_login, user_register

app_name = 'customer'

urlpatterns = [
    path('register-login/', user_register_login, name="register-login"),
    path('login/', user_login, name="login"),
    path('register/', user_register, name="register"),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('customer:register-login')), name='logout'),
    # path('courses-api/<str:text>', CourseViewSet.as_view(), name='courses-api')
]
