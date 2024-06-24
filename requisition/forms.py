from django.forms import ModelForm
from requisition.models import Requisition

class RequisitionForm(ModelForm):
    class Meta:
        model = Requisition
        fields = ('requisition_type', 'status', 'description')

        
    def __init__(self,  *args, **kwargs):
        super(RequisitionForm, self).__init__(*args, **kwargs) 
        
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"