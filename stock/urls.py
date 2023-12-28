from django.urls import path

from . import views

app_name = 'stock'

urlpatterns = [
    path('', views.GasListView.as_view(), name='gas_list'),
    path('add/', views.GasCreateView.as_view(), name='gas_create'),
    path('<int:pk>/update/', views.GasUpdateView.as_view(), name='gas_update'),
    path('<int:pk>/delete/', views.GasDeleteView.as_view(), name='gas_delete'),
]