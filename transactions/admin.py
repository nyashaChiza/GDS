from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'quantity', 'product', 'created', 'status', 'get_total_cost')
    list_filter = ('product', 'created', 'updated')
    search_fields = ('customer', 'product__name')
    readonly_fields = ('total_cost',)

    def get_total_cost(self, obj):
        return obj.total_cost()
    get_total_cost.short_description = 'Total Cost'