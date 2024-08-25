from django.forms import ModelForm
from stock.models import Reciept
from requisition.models import Requisition
from django.forms.widgets import HiddenInput

class RequisitionForm(ModelForm):
    class Meta:
        model = Requisition
        fields = ('requisition_type', 'status', 'site','description')

        
    def __init__(self,  *args, **kwargs):
        super(RequisitionForm, self).__init__(*args, **kwargs) 
        self.fields["site"].widget = HiddenInput()
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            
class RecieptForm(ModelForm):
    class Meta:
        model = Reciept
        fields = ('stock', 'quantity', 'description')

        
    def __init__(self,  *args, **kwargs):
        super(RecieptForm, self).__init__(*args, **kwargs) 
        self.fields["stock"].widget = HiddenInput()
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"