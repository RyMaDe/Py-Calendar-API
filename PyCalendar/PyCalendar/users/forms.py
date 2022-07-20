from django.forms import ModelForm
from .models import NewUser


class UpdateUserForm(ModelForm):
    class Meta:
        model = NewUser
        fields = ['email', 'first_name']
