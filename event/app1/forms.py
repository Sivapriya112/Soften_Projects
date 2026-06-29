from django import forms
from .models import Booking,AdminBooking
from datetime import date

class BookingForm(forms.ModelForm):
    advance_payment = forms.DecimalField(initial=5000, min_value=5000)
    class Meta:
        model = Booking
        fields = ['phone', 'event', 'address', 'booking_date', 'advance_payment']

        widgets = {
            'event': forms.Select(attrs={'class': 'form-control'}),
            'booking_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'advance_payment': forms.NumberInput(attrs={'class': 'form-control',
                                                        'placeholder': 'Enter advance payment'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['booking_date'].widget.attrs['min'] = date.today().isoformat()

    def clean_advance_payment(self):
        advance_payment = self.cleaned_data.get('advance_payment', 0)
        if advance_payment < 5000:
            raise forms.ValidationError("Minimum advance payment is 5000.")
        return advance_payment

    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')
        if booking_date <= date.today():
            raise forms.ValidationError("The booking date must be a future date.")
        return booking_date

class AdminBookingForm(forms.ModelForm):
    class Meta:
        model = AdminBooking
        fields = ['booking', 'tailor', 'catering', 'entertainer']
