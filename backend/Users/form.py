from django import forms
from .models import userinform

class UserInformForm(forms.ModelForm):

    class Meta:
        model = userinform
        fields = ['username', 'email', 'phone', 'birthday', 'gender']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@example.com'):
            raise forms.ValidationError("Email must be from the domain '@example.com'.")
        return email
    def clean(self):
        cleaned_data = super().clean()
        gender = cleaned_data.get('gender')
        if gender not in ['male', 'female']:
            raise forms.ValidationError("Gender must be either 'male' or 'female'.")
        return cleaned_data
    
    