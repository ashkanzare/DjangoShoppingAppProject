from django import forms
from user.models import User, UserAuthCode


class UserRegisterLogin(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserRegisterLogin, self).__init__(*args, **kwargs)
        self.fields['phone'].label = ""

    class Meta:
        model = User
        fields = ['phone']


class UserCode(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserCode, self).__init__(*args, **kwargs)
        self.fields['code'].label = ""
        self.fields['code'].initial = ""

    class Meta:
        model = UserAuthCode
        fields = ['code']


class UserPassword(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserPassword, self).__init__(*args, **kwargs)
        self.fields['password'].label = ""
        self.fields['password'].widget = forms.PasswordInput()

    class Meta:
        model = User
        fields = ['password']


class ResetPassword(forms.Form):
    password1 = forms.CharField(max_length=1000, min_length=6, label='رمز عبور جدید', widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=1000, min_length=6, label='تکرار رمز عبور جدید',
                                widget=forms.PasswordInput())
