from django.contrib import admin
from .models import Integration
from simple_history.admin import SimpleHistoryAdmin

@admin.register(Integration)
class IntegrationAdmin(SimpleHistoryAdmin):
    list_display = ['created', 'updated']
    search_fields = ['integration_id']
    readonly_fields = ['created', 'updated']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Decrypt the fields before showing in the form
        if obj:
            form.base_fields['integration_id'].initial = obj.decrypt_data(obj.integration_id)
            form.base_fields['integration_key'].initial = obj.decrypt_data(obj.integration_key)
            form.base_fields['result_url'].initial = obj.decrypt_data(obj.result_url)
            form.base_fields['return_url'].initial = obj.decrypt_data(obj.return_url)
        return form

    def save_model(self, request, obj, form, change):
        # Encrypt fields before saving
        obj.integration_id = obj.encrypt_data(form.cleaned_data['integration_id'])
        obj.integration_key = obj.encrypt_data(form.cleaned_data['integration_key'])
        obj.result_url = obj.encrypt_data(form.cleaned_data['result_url'])
        obj.return_url = obj.encrypt_data(form.cleaned_data['return_url'])
        super().save_model(request, obj, form, change)
