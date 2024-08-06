from django.contrib import admin
from .models import Requisition

@admin.register(Requisition)
class RequisitionAdmin(admin.ModelAdmin):
    list_display = ('site','requisition_type', 'status',  'created')
    list_filter = ('site','requisition_type', 'status',  'created')
    search_fields = ('site','requisition_type', 'status',  'created')
   