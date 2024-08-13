
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('optimus/', admin.site.urls),
    path('__debug__/', include("debug_toolbar.urls")),
    path('dashboard/', include('dashboard.urls')),
    path('auth/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('stock/', include('stock.urls')),
    path('transactions/', include('transactions.urls')),
    path('requisitions/', include('requisition.urls')),
        path('billing/', include('billing.urls')),
    
]
