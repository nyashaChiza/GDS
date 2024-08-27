from datetime import datetime
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from billing.models import BillingProfile
from dashboard.helpers import DashboardData
from .forms import CompanyForm, SiteForm, UserForm, StaffUserForm
from .models import Company, Site
from billing.models import BillingProfile
from stock.models import Stock
from django.views.generic import ListView, TemplateView, DetailView


def create_user(request):

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created Sucessfully")
            return redirect('create_company')
    else:
        form = UserForm()
    return render(request, 'account/signup.html', {'form': form})

@login_required
def create_staff(request, pk:int):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            site = Site.objects.get(pk=pk)  # Assuming the site is selected in the form
            staff_user = form.save(commit=False)
            staff_user.company = request.user.company
            
            # Assign the user as the site's manager or operator based on their role
            if staff_user.role == 'Manager':
                site.manager = staff_user
            elif staff_user.role == 'Operator':
                site.operator = staff_user
            staff_user.save()  # Save the user
            site.save()  # Save the site with updated manager/operator

            messages.success(request, "Account Created Successfully")
            return redirect('site_list')
        else:
            for error in form.error_messages:
                messages.warning(request, f"{error}")
            return redirect('site_list')
    else:
        messages.warning(request, "Invalid Method")
    return redirect('site_list')

@login_required
def create_company(request):
    if request.user.role == 'Admin':
        if request.method == 'POST':
            form = CompanyForm(request.POST)
            if form.is_valid():
                company = form.save(commit=False)
                company.save()  # Save the company instance first
                # Assign the company to the logged-in user
                request.user.company = company
                request.user.save()
                # Check if BillingProfile exists for the company, create if not
                billing_profile, created = BillingProfile.objects.get_or_create(
                    company=company,
                    defaults={'admin': request.user}
                )
                messages.success(request, "Company Created Successfully and Assigned to User")
                return redirect('select_subscription_plan', billing_profile_pk=billing_profile.pk)
        else:
            form = CompanyForm()
        return render(request, 'company/create.html', {'form': form})
    else:
        messages.error(request, "You do not have the right role to view this page")
        return redirect('dashboard')
        
@login_required
def create_site(request):
    if request.user.role == "Admin":
        if request.method == 'POST':
            form = SiteForm(request.POST)
            if form.is_valid():
                site = form.save(commit=False)
                # Assign the user's company to the site
                site.company = request.user.company
                
                site.save()

                # Create initial stock for the site
                Stock.objects.create(name='LP Gas', site=site, price=float(form.data['price']))

                # Redirect to the subscription plan selection view
                messages.success(request, "Site Created Successfully.")
                
                return redirect('payment_page', site_uuid=site.uuid)    # Redirect to a list view or wherever appropriate
            else:
                return render(request, 'sites/index.html', {'add_site_form': form, 'sites': Site.objects.filter(company=request.user.company).all()})

        else:
            form = SiteForm()
            add_staff_form = StaffUserForm(initial={'status': "Active"})
        return render(request, 'sites/index.html', {'add_site_form': form, 'add_staff_form': add_staff_form, 'sites': Site.objects.filter(company=request.user.company).all()})
    else:
        messages.warning(request, "You do not have the right role to perform this action")
        return redirect('site_list')

@login_required
def update_site(request, uuid):
    site = get_object_or_404(Site, uuid=uuid, company=request.user.company)

    if request.user.role == "Admin":
        if request.method == 'POST':
            form = SiteForm(request.POST, instance=site)
            if form.is_valid():
                site = form.save(commit=False)
                # Ensure the site remains associated with the user's company
                site.company = request.user.company
                site.save()

                # Update the stock price if necessary (assuming 'price' is in the form)
                stock = Stock.objects.filter(site=site, name='LP Gas').first()
                if stock:
                    stock.price = float(form.data['price'])
                    stock.save()
                
                messages.success(request, "Site Updated Successfully")
                return redirect('site_list')
            else:
                messages.error(request, "There was an error updating the site.")
                return render(request, 'sites/update.html', {'form': form, 'site': site})
        else:
            form = SiteForm(instance=site)
            add_staff_form = StaffUserForm(initial={'status':"Active"})

        return render(request, 'sites/update.html', {'form': form, 'site': site, 'add_staff_form': add_staff_form})
    else:
        messages.warning(request, "You do not have the right role to perform this action")
        return redirect('site_list')
class SiteListView(ListView):
    model = Site
    template_name = 'sites/index.html'
    context_object_name = 'sites'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['add_staff_form'] = StaffUserForm(initial={'status':"Active"})
        context['add_site_form'] = SiteForm()
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(company=self.request.user.company, status='Active')

class SiteSearchView(ListView):
    model = Site
    template_name = 'transactions/search.html'
    context_object_name = 'sites'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_staff_form'] = StaffUserForm(initial={'status':"Active"})
        context['add_site_form'] = SiteForm()
        context["search_results"] = [site for site in self.get_queryset() if site.name == self.request.GET.get("site_name")] 
        context["search_results_count"] = len(context["search_results"])
        return context
    
class SiteStatusFilterView(ListView):
    model = Site
    template_name = 'transactions/search.html'
    context_object_name = 'sales'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_staff_form'] = StaffUserForm(initial={'status':"Active"})
        context['add_site_form'] = SiteForm()
        context["search_results"] = [site for site in self.get_queryset() if site.status == self.request.GET.get("status")] 
        context["search_results_count"] = len(context["search_results"])
        return context
    
class SiteDetailView(TemplateView):
    model = Site
    template_name = 'sites/detail.html'
    context_object_name = 'site'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site'] = Site.objects.filter(uuid=kwargs.get('uuid')).first()
        context["remaining_stock"] = DashboardData(self.request.user).get_stock_data().get('current_available_Stock_quantity')
        return context
