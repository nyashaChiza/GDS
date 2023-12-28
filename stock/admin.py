from django.contrib import admin
from .models import Gas

@admin.register(Gas)
class GasAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'price', 'supplier', 'created', 'updated')
    list_filter = ('supplier', 'created', 'updated')
    search_fields = ('name', 'supplier')
    date_hierarchy = 'created'
    ordering = ('-created',)
    fields = ('name', 'quantity', 'price', 'supplier')
    readonly_fields = ('created', 'updated')