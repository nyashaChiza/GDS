from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('site','customer', 'quantity', 'product', 'created', 'status', 'get_total_cost')
    list_filter = ('site','product', 'created', 'updated')
    search_fields = ('site','customer', 'product__name')
    readonly_fields = ('total_cost',)

    def get_total_cost(self, obj):
        return obj.total_cost()
    get_total_cost.short_description = 'Total Cost'