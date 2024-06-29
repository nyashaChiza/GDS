from django.urls import path

from . import views


urlpatterns = [
    path('', views.GasListView.as_view(), name='gas_list'),
    path('add/', views.GasCreateView.as_view(), name='gas_create'),
    path('reciept/create/', views.GasCreateView.as_view(), name='reciept_create'),
    path('<int:pk>/update/', views.GasUpdateView.as_view(), name='gas_update'),
    path('<int:pk>/delete/', views.GasDeleteView.as_view(), name='gas_delete'),

    path('reciepts/', views.RecieptListView.as_view(), name='reciept_list'),
    path('reciepts/create/', views.RecieptCreateView.as_view(), name='reciept_create'),
    path('reciepts/detail/<int:pk>/', views.RecieptDetailView.as_view(), name='reciept_detail'),
    path('reciepts/delete/<int:pk>/', views.RecieptDeleteView.as_view(), name='reciept_delete'),
]