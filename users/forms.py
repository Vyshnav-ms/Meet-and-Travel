from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    aadhaar_number = forms.CharField(max_length=12, required=True, help_text='Enter 12-digit Aadhaar number')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'aadhaar_number']

    def clean_aadhaar_number(self):
        aadhaar_number = self.cleaned_data.get('aadhaar_number')
        
        # Check if the Aadhaar number is exactly 12 digits and contains only digits
        if not aadhaar_number.isdigit() or len(aadhaar_number) != 12:
            raise forms.ValidationError("Invalid Aadhaar number. Please enter a 12-digit number.")
        
        return aadhaar_number

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']

