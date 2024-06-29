from django import forms
from django.forms import ModelForm
from stock.models import Gas
from django.forms.widgets import HiddenInput
from transactions.models import Transaction

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ('product', 'quantity', 'customer', 'status')

        
    def __init__(self,  *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs) 
        self.fields["product"].widget = HiddenInput()   
        
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            
    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        if Gas.objects.first().quantity < quantity:
            raise forms.ValidationError(f"Purchased quantity is greater than the remaining stock quantity {Gas.objects.first().quantity}kg")
        return self.cleaned_data.get("quantity")