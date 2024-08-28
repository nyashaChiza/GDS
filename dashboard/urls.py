from django.urls import path
from dashboard.views import DashboardView, generate_reports, AdminDashboardView


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('admin-dash', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('reports/', generate_reports, name='report_create'),
]