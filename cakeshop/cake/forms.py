from .models import *
from django import forms
class varun(forms.ModelForm):
    class Meta:
        model=Add_Product
        fields='__all__'

class update12(forms.ModelForm):
    class Meta:
        model=dboy
        fields=['name','email','phno']