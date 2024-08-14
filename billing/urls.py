from django.urls import path
from .views import payment_success, payment_failed, select_subscription_plan

urlpatterns = [
    # Other URL patterns for your app
    
    path('payment/success/', payment_success, name='payment_success'),
    path('payment/failed/', payment_failed, name='payment_failed'),
     path('select-subscription-plan/<int:site_id>/', select_subscription_plan, name='select_subscription_plan'),
]
