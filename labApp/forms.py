from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import *
from .models import Departments,Orders


class RegistrationForm(UserCreationForm):
    username = CharField(min_length=5, label='Username')
    password1 = CharField(min_length=8, widget=PasswordInput, label='Password')
    password2 = CharField(min_length=8, widget=PasswordInput, label='Repeat password')
    email = EmailField(label='Email')
    first_name = CharField(max_length=30, label='First name')
    last_name = CharField(max_length=30, label='Last Name')

    class Meta:
        fields = [
            'username',
            'password1',
            'password2',
            'email',
            'first_name',
            'last_name'
        ]
        model = User


class AuthorizationForm(AuthenticationForm):
    username = CharField(min_length=5, label='Username')
    password = CharField(min_length=8, widget=PasswordInput, label='Password')


class AddDepartment(ModelForm):
    class Meta:
        fields = '__all__'
        model = Departments