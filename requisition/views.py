from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import ListView,UpdateView, DetailView
from django.views import View
from stock.models import Stock
from requisition.forms import RequisitionForm
from .models import Requisition
from django.urls import reverse, reverse_lazy
from dashboard.helpers import DashboardData, get_site


class RequisitionListView(ListView):
    model = Requisition
    template_name = 'requisition/index.html'
    context_object_name = 'requisitions'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_requisition_form'] = RequisitionForm()
        return context

    def get_queryset(self):
        site = get_site(self.request.user)
        if site:
            return super().get_queryset().filter(site=site)
        else:
            return super().get_queryset()
    
class RequisitionSearchView(ListView):
    model = Requisition
    template_name = 'requisition/search.html'
    context_object_name = 'requisitions'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_requisition_form'] = RequisitionForm()
        context["search_results"] = [requisition for requisition in self.get_queryset() if requisition.requisition_type == self.request.GET.get("type").capitalize()] 
        context["search_results_count"] = len(context["search_results"])
        return context
    
class RequisitionStatusFilterView(ListView):
    model = Requisition
    template_name = 'requisition/search.html'
    context_object_name = 'requisitions'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_requisition_form'] = RequisitionForm()
        context["search_results"] = [requisition for requisition in self.get_queryset() if requisition.status == self.request.GET.get("status")] 
        context["search_results_count"] = len(context["search_results"])
        return context

class RequisitionDetailView(DetailView):
    model = Requisition
    template_name = 'requisition/details.html'
    context_object_name = 'requisition'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["remaining_stock"] = DashboardData(self.request.user).get_stock_data().get('current_available_Stock_quantity')
        return context

class RequisitionCreateView(View):
   def post(self, request):
        form = RequisitionForm(request.POST)
        if form.is_valid():
           form.save()
           messages.success(request, "Requisition Saved Successfully") # type: ignore
        else:
            messages.warning(request, "An Error Occurred, Please Try Again") # type: ignore
            settings.LOGGER.error(form.errors)
        return redirect(reverse('requisition_list'))
    
class RequisitionUpdateStatusView(View):
       def get(self, request, pk):
        requisition = Requisition.objects.filter(pk=pk).first()
        status = request.GET.get('status')
    
        if requisition:
            requisition.status = status    
            requisition.save()
            messages.success(request, f"Requisition Marked as {status} Successfully") # type: ignore
           
        else:
            messages.warning(request, "An Error Occurred, Please Try Again") # type: ignore
        
        return redirect(reverse('requisition_list'))

class RequisitionUpdateView(UpdateView):
    model = Requisition
    template_name = 'requisition/update.html'
    form_class = RequisitionForm
    context_object_name = 'sale'
    success_url = reverse_lazy('requisition_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["remaining_stock"] = DashboardData(self.request.user).get_stock_data().get('current_available_Stock_quantity')
        return context

class RequisitionDeleteView(View):
       def get(self, request, pk):
        requisition = Requisition.objects.filter(pk=pk).first()
    
        if requisition:
           requisition.status = 'Deleted'
           requisition.delete()
           messages.success(request, "Requisition Deleted Successfully") # type: ignore
           
        else:
            messages.warning(request, "An Error Occurred, Please Try Again") # type: ignore
        
        return redirect(reverse('requisition_list'))