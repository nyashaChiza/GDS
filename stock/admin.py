from django.contrib import admin
from .models import Gas, Reciept

@admin.register(Gas)
class GasAdmin(admin.ModelAdmin):
    list_display = ('site','name', 'quantity', 'price', 'supplier', 'created', 'updated')
    list_filter = ('site','supplier', 'created', 'updated')
    search_fields = ('site','name', 'supplier')
    date_hierarchy = 'created'
    ordering = ('-created',)
    fields = ('site','name', 'quantity', 'price', 'supplier')
    readonly_fields = ('created', 'updated')
    
    
@admin.register(Reciept)
class RecieptAdmin(admin.ModelAdmin):
    list_display = ('site','quantity', 'stock', 'created')
    list_filter = ('site','quantity', 'created')
    search_fields = ('site','quantity', 'created')
    