from django.urls import path
from .views import AdvisorRegistration, AdvisorLogin, AdvisorClientRegistration, AdvisorProductPurchase

urlpatterns = [
    path('register/', AdvisorRegistration.as_view(), name='advisor-registration'),
    path('login/', AdvisorLogin.as_view(), name='advisor-login'),
    path('add_client/', AdvisorClientRegistration.as_view(), name='advisor-add_client'),
    path('product_purchase/', AdvisorProductPurchase.as_view(), name='advisor-product-purchase')
]
