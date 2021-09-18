from django import forms
from user.models import User, UserAuthCode


class UserLogin(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserLogin, self).__init__(*args, **kwargs)
        self.fields['phone'].label = ""

    class Meta:
        model = User
        fields = ['phone']


class UserCode(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserCode, self).__init__(*args, **kwargs)
        self.fields['code'].label = ""
        self.fields['code']. initial = ""

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
