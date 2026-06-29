import re
from django import forms
from .models import*
class developerform(forms.ModelForm):
    class Meta:
        model = developerregister
        fields = ['name','email','phone','skills','experience','image','bio','username','password']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Skills'}),
            'experience': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Experience'}),
            'image': forms.FileInput(attrs={'class': 'd-none', 'id': 'imageUpload'}),
            'bio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bio'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password',
            }),
        }

    # ✅ Email validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise forms.ValidationError("Enter a valid email")
        return email

    # ✅ Phone validation
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^[0-9]{10}$', phone):
            raise forms.ValidationError("Phone must be 10 digits")
        return phone

    # ✅ Password validation
    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #
    #     if len(password) < 6:
    #         raise forms.ValidationError("Minimum 6 characters")
    #
    #     if not re.search(r'[A-Z]', password):
    #         raise forms.ValidationError("Add uppercase letter")
    #
    #     if not re.search(r'[a-z]', password):
    #         raise forms.ValidationError("Add lowercase letter")
    #
    #     if not re.search(r'[0-9]', password):
    #         raise forms.ValidationError("Add number")
    #
    #     return password


class updateportfolioform(forms.ModelForm):
    class Meta:
        model=developerportfolio
        fields=['project_title','project_description','project_type','project_technology','project_duration','project_demo']
        widgets = {
            'project_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'project_title'}),
            'project_description': forms.Textarea(attrs={
                    'class': 'form-control',
                    'placeholder': 'project_description',
                    'rows': 4
                }),
             'project_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Project Type'
            }),
            'project_technology': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Technology Used'
            }),
            'project_duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duration'
            }),
            'project_demo': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Demo Link'
            }),
        }


