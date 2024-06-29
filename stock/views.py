from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View, DeleteView
from .models import Gas, Reciept
from django.contrib import messages
from requisition.forms import RecieptForm
from django.conf import settings
from django.shortcuts import redirect
from dashboard.helpers import DashboardData
from datetime import datetime


class GasListView(ListView):
    model = Gas
    template_name = 'stock/index.html'
    context_object_name = 'gas_items'

class GasCreateView(CreateView):
    model = Gas
    template_name = 'stock/create.html'
    fields = ['name', 'quantity', 'price', 'supplier']
    success_url = reverse_lazy('gas_list')

class GasUpdateView(UpdateView):
    model = Gas
    template_name = 'stock/update.html'
    fields = ['name', 'quantity', 'price', 'supplier']
    success_url = reverse_lazy('gas_list')

class GasDeleteView(DeleteView):
    model = Gas
    template_name = 'stock/delete.html'
    success_url = reverse_lazy('gas_list')
    
    
class RecieptListView(ListView):
    model = Reciept
    template_name = 'reciept/index.html'
    context_object_name = 'reciepts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_reciept_form'] = RecieptForm(initial={"stock":Gas.objects.first()})
        return context
    
class RecieptCreateView(View):
       def post(self, request):
        form = RecieptForm(request.POST)
        if form.is_valid():
            form.save()
            gas_stock = Gas.objects.filter(pk=form.instance.stock.pk).first()
            if gas_stock:
                gas_stock.quantity =  form.instance.stock.quantity + form.instance.quantity
                gas_stock.save()
                settings.LOGGER.critical(form.instance.stock.quantity)
                
            messages.success(request, "Receipt Saved Successfully") # type: ignore
        else:
            messages.warning(request, "An Error Occurred, Please Try Again") # type: ignore
            settings.LOGGER.error(form.errors)
        return redirect(reverse('reciept_list'))


class RecieptDetailView(DetailView):
    model = Reciept
    template_name = 'reciept/detail.html'
    context_object_name = 'reciept'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["remaining_stock"] = DashboardData(datetime.now()).get_stock_data().get('current_available_gas_quantity')
        return context
    
class RecieptDeleteView(View):
       def get(self, request, pk):
        reciept = Reciept.objects.filter(pk=pk).first()
        stock = Gas.objects.filter(pk=reciept.stock.pk).first()
        if reciept.stock.quantity - reciept.quantity > -1:
            stock.quantity = reciept.stock.quantity - reciept.quantity
            stock.save()    
        reciept.delete()    
        messages.success(request, "Reciept Deleted Successfully") # type: ignore        
        return redirect(reverse('reciept_list'))