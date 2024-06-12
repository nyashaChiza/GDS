from django.forms import ModelForm
from transactions.models import Transaction

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ('product', 'quantity', 'customer', 'status')

        
    def __init__(self,  *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)    
        
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"