from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from dashboard.helpers import DashboardData
from datetime import datetime
from django.contrib import messages

@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is an Admin
        if request.user.role == 'Admin':
            # Check if the admin has a company set up
            if not request.user.company:
                return redirect('create_company')
        
        # Check if the user is a Manager or Operator
        if request.user.role in ['Manager', 'Operator']:
            # Check if the manager/operator has a company and site assigned
            if not request.user.company or not request.user.site:
                # Show a banner/message
                messages.info(request, "Please contact your admin to set up your company and site.")
                return redirect('account_login')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dashboard_data'] = DashboardData(self.request.user, datetime.now())
        return context
