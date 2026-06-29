from django import forms


from.models import *

class modelform(forms.ModelForm):
    class Meta:
        model = addproduct
        fields = '__all__'
