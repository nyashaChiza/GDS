from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Gas

class GasListView(ListView):
    model = Gas
    template_name = 'stock/index.html'
    context_object_name = 'gas_items'

class GasCreateView(CreateView):
    model = Gas
    template_name = 'stock/create.html'
    fields = ['name', 'quantity', 'price', 'supplier']
    success_url = reverse_lazy('stock:gas_list')

class GasUpdateView(UpdateView):
    model = Gas
    template_name = 'stock/update.html'
    fields = ['name', 'quantity', 'price', 'supplier']
    success_url = reverse_lazy('stock:gas_list')

class GasDeleteView(DeleteView):
    model = Gas
    template_name = 'stock/delete.html'
    success_url = reverse_lazy('stock:gas_list')