from django.urls import path
from .views import payment_success, payment_failed

urlpatterns = [
    # Other URL patterns for your app
    
    path('payment/success/', payment_success, name='payment_success'),
    path('payment/failed/', payment_failed, name='payment_failed'),
]
