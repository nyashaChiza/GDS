from django.urls import path
from . import views

urlpatterns = [
    path('', views.RequisitionListView.as_view(), name='requisition_list'),
    path('search/', views.RequisitionSearchView.as_view(), name='requisition_search'),
    path('filter/', views.RequisitionStatusFilterView.as_view(), name='requisition_filter'),
    path('create/', views.RequisitionCreateView.as_view(), name='requisition_create'),
    path('<int:pk>/detail/', views.RequisitionDetailView.as_view(), name='requisition_detail'),
    path('<int:pk>/update/', views.RequisitionUpdateView.as_view(), name='requisition_update'),
    path('<int:pk>/status/update/', views.RequisitionUpdateStatusView.as_view(), name='review_requisition'),
    path('<int:pk>/delete/', views.RequisitionDeleteView.as_view(), name='requisition_delete'),


]