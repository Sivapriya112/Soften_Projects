
from django import forms
from .models import *


class edit_image(forms.ModelForm):
    class Meta:
        model=fish
        fields=['fishname','fprice','fstock','fimage','category']

