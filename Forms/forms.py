from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from toilet.models import Toilet

from django.forms import ModelForm


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ToiletForm(ModelForm):
    class Meta:
        model = Toilet
        fields = ['category', 'place']
