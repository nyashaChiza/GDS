from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from dashboard.helpers import DashboardData


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'
    
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if user.role == 'Admin':
            # Admin must have a company set up
            if not user.company:
                return redirect('create_company')

        elif user.role in ['Manager', 'Operator']:
            # Manager or Operator must have a company and a site assigned
            if not user.company or (user.role == 'Manager' and not user.managed_site) or (user.role == 'Operator' and not user.operation_site):
                messages.info(request, "Please contact your admin to set up your company and site.")
                return redirect('account_login')

        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dashboard_data'] = DashboardData(self.request.user)
        context['month']= datetime.now().strftime('%B')
        return context
    
    

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

