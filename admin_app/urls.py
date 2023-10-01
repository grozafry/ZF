from django.urls import path
from .views import AdminProductCreation, AdminRegistration, AdminLogin

urlpatterns = [
    path('create_product/', AdminProductCreation.as_view(), name='create-product'),
    path('register/', AdminRegistration.as_view(), name='admin-registration'),
    path('login/', AdminLogin.as_view(), name='admin-login'),
]
