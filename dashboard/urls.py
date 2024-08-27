from django.urls import path
from dashboard.views import DashboardView, generate_reports


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('reports/', generate_reports, name='report_create'),
]