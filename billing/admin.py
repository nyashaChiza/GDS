from django.contrib import admin
from .models import SubscriptionPlan, BillingProfile, Invoice, Payment

class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_site', 'max_sites', 'created', 'updated')
    search_fields = ('name',)
    list_filter = ('created', 'updated')
    ordering = ('-created',)
    readonly_fields = ('created', 'updated')

class BillingProfileAdmin(admin.ModelAdmin):
    list_display = ('company', 'subscription_plan', 'subscription_status', 'last_payment_date', 'created', 'updated')
    search_fields = ('company__name', 'subscription_plan__name')
    list_filter = ('subscription_status', 'created', 'updated')
    readonly_fields = ('created', 'updated')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Optionally filter queryset here if needed
        return queryset
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'billing_profile', 'date_issued', 'amount_due', 'due_date', 'currency', 'status', 'created', 'updated')
    search_fields = ('uuid', 'billing_profile__company__name', 'currency')
    list_filter = ('status', 'currency', 'created', 'updated')
    readonly_fields = ('uuid', 'created', 'updated')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Optionally filter queryset here if needed
        return queryset
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'invoice', 'payment_method', 'created', 'updated')
    search_fields = ('invoice__uuid', 'payment_method')
    list_filter = ('payment_method', 'created', 'updated')
    readonly_fields = ('uuid', 'created', 'updated')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Optionally filter queryset here if needed
        return queryset
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()

# Register models with their respective admin classes
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(BillingProfile, BillingProfileAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Payment, PaymentAdmin)
