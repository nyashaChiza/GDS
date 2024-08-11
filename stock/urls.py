from django.urls import path

from . import views


urlpatterns = [
    path('', views.StockListView.as_view(), name='Stock_list'),
    path('add/', views.StockCreateView.as_view(), name='Stock_create'),
    path('reciept/create/', views.StockCreateView.as_view(), name='reciept_create'),
    path('<int:pk>/update/', views.StockUpdateView.as_view(), name='Stock_update'),
    path('<int:pk>/delete/', views.StockDeleteView.as_view(), name='Stock_delete'),

    path('reciepts/', views.RecieptListView.as_view(), name='reciept_list'),
    path('reciepts/create/', views.RecieptCreateView.as_view(), name='reciept_create'),
    path('reciepts/detail/<int:pk>/', views.RecieptDetailView.as_view(), name='reciept_detail'),
    path('reciepts/delete/<int:pk>/', views.RecieptDeleteView.as_view(), name='reciept_delete'),
]