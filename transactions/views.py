from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Transaction
from django.urls import reverse_lazy

class TransactionListView(ListView):
    model = Transaction
    template_name = 'transactions/index.html'
    context_object_name = 'sales'

class TransactionCreateView(CreateView):
    model = Transaction
    template_name = 'transactions/create.html'
    fields = ['date', 'product', 'quantity', 'unit_cost']
    success_url = reverse_lazy('transactions:transaction_list')

class TransactionUpdateView(UpdateView):
    model = Transaction
    template_name = 'transactions/update.html'
    fields = ['date', 'product', 'quantity', 'unit_cost']
    success_url = reverse_lazy('transactions:transaction_list')

class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'transactions/delete.html'
    success_url = reverse_lazy('transactions:transaction_list')