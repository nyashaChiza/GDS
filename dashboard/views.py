from django.views.generic import TemplateView
from dashboard.helpers import DashboardData
from datetime import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.template import loader

from .helpers import generate_inventory_report, generate_requisition_report, generate_sales_report
class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
     
        context['dashboard_data'] = DashboardData(datetime.now())
        return context
    
    
@csrf_protect
def generate_reports(request):
    if request.method == 'POST':
        month = request.POST.get('month')
        report_type = request.POST.get('report_type')

        # Logic to generate the report based on month and report_type
        # This is just an example, implement your own report generation logic
        if report_type == 'sales_report':
            report = generate_sales_report(month)
        elif report_type == 'requisition_report':
            report = generate_requisition_report(month)
        elif report_type == 'inventory_report':
            report = generate_inventory_report(month)
        else:
            report = "Invalid report type selected."

        # Return the report as an HTTP response
        return report

