from django import forms
from app.models import *

class User_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','password']
        widgets = {'password': forms.PasswordInput}
        help_texts = {'username':''}
        label_suffix = '-'

class Profile_Form(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address','profile_pic']
        label_suffix = ' '