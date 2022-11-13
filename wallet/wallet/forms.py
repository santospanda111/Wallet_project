from django import forms
from django.contrib.auth.models import User
from .models import Owner, Transfer
from django.core.validators import RegexValidator


class UserReg(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, validators=[RegexValidator(regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,20}', message="Password should contain Minimum 8 characters, at least 1 Uppercase Alphabet, 1 Lowercase Alphabet, 1 Number and 1 Special Character")])
    username = forms.CharField(min_length=5)
    usertype = forms.CharField()

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError("This username is already registered with us")
        return data

    class Meta:
        model = User
        fields = ['username', 'password']

class OwnerInfo(forms.ModelForm):

    class Meta:
        model = Owner
        fields = ['name']

class TransferBalance(forms.ModelForm):

    class Meta:
        model = Transfer
        fields = ['username', 'transfer_amount']
