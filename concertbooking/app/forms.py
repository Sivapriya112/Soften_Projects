from django import forms
from .models import *


class modelform(forms.ModelForm):
    class Meta:
        model=Events
        fields=['Event_name','Location','Date','Time','Gold_Ticket_price','Silver_Ticket_price','Bronze_Ticket_price','Gold_Available_tickets','Silver_Available_tickets','Bronze_Available_tickets','Event_image','Sub_images','Video']