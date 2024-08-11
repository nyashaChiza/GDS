from django.contrib import messages
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView,UpdateView, DetailView
from django.views import View
from transactions.forms import TransactionForm
from .models import Transaction
from stock.models import Stock
from django.urls import reverse, reverse_lazy
from dashboard.helpers import DashboardData
from dashboard.helpers import get_site

class TransactionListView(ListView):
    model = Transaction
    template_name = 'transactions/index.html'
    context_object_name = 'sales'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = get_site(self.request.user)
        if site:
            context['add_sale_form'] = TransactionForm(initial={"product":site.stock.first()})
            context['remaining_quantity'] = site.stock.first().quantity
        else:
            context['add_sale_form'] = TransactionForm()

        return context
    
    def get_queryset(self):
        site = get_site(self.request.user)
        if site:
            return super().get_queryset().filter(site=site)
        else:
            return super().get_queryset()
    
class TransactionSearchView(ListView):
    model = Transaction
    template_name = 'transactions/search.html'
    context_object_name = 'sales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_sale_form'] = TransactionForm(initial={"product":Stock.objects.first()})
        context["search_results"] = [sale for sale in self.get_queryset() if sale.order_number() == self.request.GET.get("order_number")] 
        context["search_results_count"] = len(context["search_results"])
        return context
    
class TransactionStatusFilterView(ListView):
    model = Transaction
    template_name = 'transactions/search.html'
    context_object_name = 'sales'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_sale_form'] = TransactionForm(initial={"product":Stock.objects.first()})
        context["search_results"] = [sale for sale in self.get_queryset() if sale.status == self.request.GET.get("status")] 
        context["search_results_count"] = len(context["search_results"])
        return context

class TransactionDetailView(DetailView):
    model = Transaction
    template_name = 'transactions/details.html'
    context_object_name = 'sale'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["remaining_stock"] = DashboardData(self.request.user).get_stock_data().get('current_available_Stock_quantity')
        return context    

class TransactionCreateView(View):
    def post(self, request):
        form = TransactionForm(request.POST)
        
        if form.is_valid():
            site = get_site(request.user)
            if not site:
                messages.warning(request, "Invalid user role or site association.")
                return redirect(reverse('transaction_list'))
            
            stock = site.stock.first()  # Assuming the site has a related stock object
            quantity = form.cleaned_data['quantity']
            
            # Perform the quantity validation
            if stock and stock.quantity >= quantity:
                # Decrement the stock quantity
                stock.quantity -= quantity
                stock.save()

                # Save the transaction
                transaction = form.save(commit=False)
                transaction.site = site
                transaction.save()

                messages.success(request, "Sale Saved Successfully")
            else:
                messages.warning(request, f"Insufficient stock quantity. Available quantity: {stock.quantity}kg")
        else:
            messages.warning(request, "Failed to save the transaction. Please correct the errors below.")
            messages.warning(request, form.errors)

        return redirect(reverse('transaction_list'))

class TransactionUpdateStatusView(View):
       def get(self, request, pk):
        transaction = Transaction.objects.filter(pk=pk).first()
    
        if transaction:
           transaction.status = 'Paid'
           transaction.save()
           messages.success(request, "Sale Marked as Paid Successfully") # type: ignore
           
        else:
            messages.warning(request, "An Error Occurred, Please Try Again") # type: ignore
        
        return redirect(reverse('transaction_list'))

class TransactionUpdateView(UpdateView):
    model = Transaction
    template_name = 'transactions/update.html'
    form_class = TransactionForm
    context_object_name = 'sale'
    success_url = reverse_lazy('transaction_list')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["remaining_stock"] = DashboardData(self.request.user).get_stock_data().get('current_available_Stock_quantity')
        return context

class TransactionDeleteView(View):
       def get(self, request, pk):
        transaction = Transaction.objects.filter(pk=pk).first()
    
        if transaction:
           transaction.status = 'Deleted'
           transaction.delete()
           messages.success(request, "Sale Deleted Successfully") # type: ignore
           
        else:
            messages.warning(request, "An Error Occurred, Please Try Again") # type: ignore
        
        return redirect(reverse('transaction_list'))