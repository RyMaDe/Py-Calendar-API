from django.forms import ModelForm
from django import forms
from .models import NewUser


class UpdateUserForm(ModelForm):
    class Meta:
        model = NewUser
        fields = ['email', 'first_name']


class UpdateUserPasswordForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
    attrs={'class':'form-control','type':'password', 'name': 'password','placeholder':'Password'}),
    label='')

    class Meta:
        model = NewUser
        fields = ['password']

    def save(self, commit=True):
        user = super(UpdateUserPasswordForm, self).save(commit=False)
        cleaned_data = self.cleaned_data
        password = cleaned_data.pop('password', None)
        if password is not None:
            user.set_password(password)
        if commit:
            user.save()
        return user
