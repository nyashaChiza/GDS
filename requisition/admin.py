from django.contrib import admin
from .models import Requisition

@admin.register(Requisition)
class RequisitionAdmin(admin.ModelAdmin):
    list_display = ('requisition_type', 'status',  'created')
    list_filter = ('requisition_type', 'status',  'created')
    search_fields = ('requisition_type', 'status',  'created')
   