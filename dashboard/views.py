from django.views.generic import TemplateView
from dashboard.helpers import DashboardData
from datetime import datetime

class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
     
        context['dashboard_data'] = DashboardData(datetime.now())
        return context
    