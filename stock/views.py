from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View, DeleteView
from .models import Stock, Reciept
from django.contrib import messages
from requisition.forms import RecieptForm
from django.conf import settings
from django.shortcuts import redirect
from dashboard.helpers import DashboardData, get_site



class StockListView(ListView):
    model = Stock
    template_name = 'stock/index.html'
    context_object_name = 'Stock_items'
    
    def get_queryset(self):
        site = get_site(self.request.user)
        if site:
            return super().get_queryset().filter(site=site)
        else:
            return super().get_queryset()

class StockCreateView(CreateView):
    model = Stock
    template_name = 'stock/create.html'
    fields = ['name', 'quantity', 'price', 'supplier']
    success_url = reverse_lazy('Stock_list')

class StockUpdateView(UpdateView):
    model = Stock
    template_name = 'stock/update.html'
    fields = ['name', 'quantity', 'price', 'supplier']
    success_url = reverse_lazy('Stock_list')

class StockDeleteView(DeleteView):
    model = Stock
    template_name = 'stock/delete.html'
    success_url = reverse_lazy('Stock_list')
    
    
class RecieptListView(ListView):
    model = Reciept
    template_name = 'reciept/index.html'
    context_object_name = 'reciepts'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = get_site(self.request.user)
        if site:
            context['add_reciept_form'] = RecieptForm(initial={"stock":site.stock.first(), "site":site})
        else:
            context['add_reciept_form'] = RecieptForm()
        return context
    
    def get_queryset(self):
        site = get_site(self.request.user)
        if site:
            return super().get_queryset().filter(site=site)
        else:
            return super().get_queryset()
    
class RecieptCreateView(View):
       def post(self, request):
        form = RecieptForm(request.POST)
        if form.is_valid():
            form.save()
            stock = Stock.objects.filter(pk=form.instance.stock.pk).first()
            if stock:
                stock.quantity =  stock.quantity + form.instance.quantity
                receipt = form.save(commit=False)
                receipt.site = get_site(self.request.user)
                stock.save()
                receipt.save()
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
        context["remaining_stock"] = DashboardData(self.request.user).get_stock_data().get('current_available_Stock_quantity')
        return context
    
class RecieptDeleteView(View):
       def get(self, request, pk):
        reciept = Reciept.objects.filter(pk=pk).first()
        stock = Stock.objects.filter(pk=reciept.stock.pk, site=request.user.site).first()
        if reciept.stock.quantity - reciept.quantity > -1:
            stock.quantity = reciept.stock.quantity - reciept.quantity
            stock.save()    
        reciept.delete()    
        messages.success(request, "Reciept Deleted Successfully") # type: ignore        
        return redirect(reverse('reciept_list'))