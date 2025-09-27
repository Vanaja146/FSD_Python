# website/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import AuthUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        # Use your custom AuthUser model
        model = AuthUser
        # The fields the user will fill out during signup
        # Note: UserCreationForm automatically handles the password fields.
        fields = ('username', 'email') 

    # Custom validation to ensure the email address is unique
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if AuthUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    # We must explicitly add the email field to the form's helper class
    # to make it required by default, but it's good practice to ensure it's
    # handled correctly by UserCreationForm inheritance.