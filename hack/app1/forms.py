from django import forms
from .models import *

class normalform(forms.Form):
    name = forms.CharField(max_length=30)
    price = forms.IntegerField()
    quantity = forms.IntegerField()
    image = forms.IntegerField()

class modelform(forms.ModelForm):
    class Meta:
        model=add_product
        fields='__all__'