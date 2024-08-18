from django.urls import path
from .views import payment_success, payment_failed, select_subscription_plan, payment_page

urlpatterns = [
    # Other URL patterns for your app
    
    path('payment/success/', payment_success, name='payment_success'),
    path('payment/failed/', payment_failed, name='payment_failed'),
    path('select-subscription-plan/<int:billing_profile_pk>/', select_subscription_plan, name='select_subscription_plan'),
    path('payment/<uuid:site_uuid>/', payment_page, name='payment_page') 
]
