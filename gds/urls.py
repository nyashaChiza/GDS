
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include("debug_toolbar.urls")),
    path('', include('dashboard.urls')),
    path('accounts/', include('allauth.urls')),
    path('stock/', include('stock.urls')),
    path('transactions/', include('transactions.urls')),
    path('requisitions/', include('requisition.urls')),
    
]
