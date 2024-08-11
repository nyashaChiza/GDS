from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'gender', 'display_picture', 'role', 'status']
        
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Set the role field to be hidden and default to 'Admin'
        self.fields['role'] = forms.CharField(widget=forms.HiddenInput(), initial='Admin')
        self.fields['status'] = forms.CharField(widget=forms.HiddenInput(), initial='Active')

class StaffUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'company','phone_number', 'gender', 'display_picture', 'role', 'status']
        
    def __init__(self, *args, **kwargs):
        super(StaffUserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
        self.fields['status'] = forms.CharField(widget=forms.HiddenInput(), initial='Active')
        self.fields['site'] = forms.CharField(widget=forms.HiddenInput())
        self.fields['company'] = forms.CharField(widget=forms.HiddenInput())
