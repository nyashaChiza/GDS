from django.urls import path
from . import views

# app_name = 'transactions'

urlpatterns = [
    path('', views.TransactionListView.as_view(), name='transaction_list'),
    
    path('search/', views.TransactionSearchView.as_view(), name='transaction_search'),
    path('filter/', views.TransactionStatusFilterView.as_view(), name='transaction_filter'),
    path('create/', views.TransactionCreateView.as_view(), name='transaction_create'),
    path('<int:pk>/detail/', views.TransactionDetailView.as_view(), name='transaction_detail'),
    path('<int:pk>/update/', views.TransactionUpdateView.as_view(), name='transaction_update'),
    path('<int:pk>/status/update/', views.TransactionUpdateStatusView.as_view(), name='mark_sale_as_paid'),
    path('<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='transaction_delete'),
]