from django import forms
from accounts.models import Company, Site

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'address', 'contact']
        
    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['name', 'address', 'contact', 'capacity']
    def __init__(self, *args, **kwargs):
        super(SiteForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            
        self.fields['company'] = forms.CharField(widget=forms.HiddenInput())