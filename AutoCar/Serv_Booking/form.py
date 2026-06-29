
from django import forms # type: ignore
from .models import *  # noqa: F403
from django.contrib import admin

class SampleForm(forms.ModelForm):
    class Meta:
        model = Products  # noqa: F405
        fields = ['product_name', 'product_price', 'product_image', 'quantity', 'product_details']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter product name'}),
            'product_price': forms.TextInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter product price'}),
            'product_image': forms.FileInput(attrs={'class': 'form-control form-manual input'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter quantity'}),
            'product_details': forms.Textarea(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter product details'}),
        }

class user_address(forms.ModelForm):
    class Meta:
        model = user_details  # noqa: F405
        fields = ['housename','landmark','area','pincode']
        widgets = {
            'housename': forms.TextInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter product house name'}),
            'landmark': forms.TextInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter product landmark'}),
            'area': forms.TextInput(attrs={'class': 'form-control form-manual input','placeholder': 'Enter product area'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter Pincode'})
         }
        
class user_profile(forms.ModelForm):
    class Meta:
        model = user_details #noqa
        fields = ['name', 'email', 'phone_no','username', 'user_image','housename','landmark','area', 'pincode']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter product name'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter product email address'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter product Phone number'}),
            'username': forms.TextInput(attrs={'class': 'form-control form-manual input','placeholder': 'Enter product username'}),
            'housename': forms.TextInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter product house name'}),
            'landmark': forms.TextInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter product landmark'}),
            'area': forms.TextInput(attrs={'class': 'form-control form-manual input','placeholder': 'Enter product area'}),
        #    'housename': forms.Textarea(attrs={
        #         'class': 'form-control form-manual textare', 
        #         'placeholder': 'Enter product address',
        #         'rows': 8,  # Optional: Specify the number of rows
        #         'cols': 50  # Optional: Specify the number of columns
        #     }),
            'user_image': forms.FileInput(attrs={'class': 'form-control form-manual input'}),
           
            'pincode': forms.TextInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter product Pincode'})
        }
        
        

# ================================Delivery Boy =====================================


class DBoyDetails(forms.ModelForm):
    class Meta:
        model = DeliveryBoy #noqa
        fields = ['name', 'email', 'phone','username', 'profile_picture','address', 'license_image','status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter product name'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter product email address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter product Phone number'}),
            'username': forms.TextInput(attrs={'class': 'form-control form-manual input', 'readonly': 'readonly','placeholder': 'Enter product username'}),
           'address': forms.Textarea(attrs={
                'class': 'form-control form-manual textare', 
                'placeholder': 'Enter product address',
                'rows': 8,  # Optional: Specify the number of rows
                'cols': 50  # Optional: Specify the number of columns
            }),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control form-manual input'}),
            # 'license_image': forms.FileInput(attrs={'class': 'form-control form-manual input'}),
           
           
            'status': forms.TextInput(attrs={'class': 'form-control form-manual input','readonly': 'readonly', 'placeholder': 'Enter product Pincode'})
        }
        
from django import forms



class ProductImageForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['product_image']
        widgets = {
             'product_image': forms.FileInput(attrs={'class': 'form-control form-manual input'})
         }

class ProductForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Products
        fields = ['car_name', 'product_name', 'product_image', 'product_price', 'product_details', 'quantity', 'status']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter product name'}),
            'product_details': forms.Textarea(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter product details', 'rows': 3}),
            'product_price': forms.NumberInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter product price'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter product quantity'}),
            'status': forms.TextInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter product status'}),
            'car_name': forms.TextInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter car name'}),
            'product_image': forms.ClearableFileInput(attrs={'class': 'form-control-file form-manual input', 'accept': 'image/*'}),
        }

    def clean_product_image(self):
        # Handle optional file upload for product_image
        product_image = self.cleaned_data.get('product_image')
        if not product_image:
            # If no image is uploaded, return None
            return None
        return product_image




class ServiceForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = services
        fields = ['service_name', 'service_image', 'service_discription', 'service_amount', 'status']
        widgets = {
            'service_name': forms.TextInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter service name'}),
            'service_discription': forms.Textarea(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter service details', 'rows': 3}),
            'service_amount': forms.NumberInput(attrs={'class': 'form-control form-manual input', 'placeholder': 'Enter service price'}),
            'status': forms.Select(attrs={'class': 'form-control form-manual input'}),
            'service_image': forms.ClearableFileInput(attrs={'class': 'form-control-file form-manual input', 'accept': 'image/*'}),
        }

    def clean_service_image(self):
        service_image = self.cleaned_data.get('service_image')
        if not service_image:
            return None
        return service_image

