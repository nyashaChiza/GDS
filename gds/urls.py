
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView


urlpatterns = [
    path('optimus/', admin.site.urls),
    path('__debug__/', include("debug_toolbar.urls")),
    path('dashboard/', include('dashboard.urls')),
    path('', RedirectView.as_view(url='/auth/login/', permanent=False), name='landing'),
    path('auth/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('stock/', include('stock.urls')),
    path('transactions/', include('transactions.urls')),
    path('requisitions/', include('requisition.urls')),
    path('billing/', include('billing.urls')),
]
