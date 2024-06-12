from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import ListView,UpdateView, DeleteView
from django.views import View
from transactions.forms import TransactionForm
from .models import Transaction
from stock.models import Gas
from django.urls import reverse, reverse_lazy

class TransactionListView(ListView):
    model = Transaction
    template_name = 'transactions/index.html'
    context_object_name = 'sales'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_sale_form'] = TransactionForm(initial={"product":Gas.objects.first()})
        return context

class TransactionCreateView(View):
   def post(self, request):
        form = TransactionForm(request.POST)
        if form.is_valid():
           form.save()
           messages.success(request, "Sale Saved Successfully") # type: ignore
        else:
            messages.warning(request, "An Error Occurred, Please Try Again") # type: ignore
            settings.LOGGER.error(form.errors)
        return reverse('transaction_list')
    
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
    fields = ['date', 'product', 'quantity', 'unit_cost']
    success_url = reverse_lazy('transaction_list')

class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'transactions/delete.html'
    success_url = reverse_lazy('transaction_list')