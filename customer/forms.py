from django import forms
from user.models import User, UserAuthCode


class UserLogin(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone']


class UserCode(forms.ModelForm):
    class Meta:
        model = UserAuthCode
        fields = ['code']
