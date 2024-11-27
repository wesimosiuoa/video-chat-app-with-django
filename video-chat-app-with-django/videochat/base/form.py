from django import forms
from .models import User

class UserForm (forms.ModelForm): 
    class Meta: 
        model = User
        field = ['email', 'password', 'username']
        widgets = {
            'password' : forms.PasswordInput(),
        }