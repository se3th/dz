from django import forms
from .models import *


class RegisterForm(forms.ModelForm):
    class Meta:
        model = CustomerModel
        exclude = ["computers", "login", "password", "secondname", "firstname"]

    firstname = forms.CharField(label="Имя", )
    secondname = forms.CharField(label="Фамилия", )
    email = forms.EmailField(label="e-mail")
    login = forms.CharField(min_length=5, label="Логин", )
    password = forms.CharField(min_length=8, widget=forms.PasswordInput, label="Введите пароль", )
    password2 = forms.CharField(min_length=8, widget=forms.PasswordInput, label="Повторите пароль", )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['firstname'].widget.attrs.update({'class' : 'form-control', 'placeholder':'Введите Имя'})
        self.fields['secondname'].widget.attrs.update({'class': 'form-control', 'placeholder':'Введите Фамилию'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите Ваш email'})
        self.fields['login'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите Логин'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Повторите пароль'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Пароль'})


class AuthorizeForm(forms.ModelForm):
    class Meta:
        model = CustomerModel
        exclude = ["computers", "firstname", "secondname", "email"]

    login = forms.CharField(min_length=5, label="Логин", )
    password = forms.CharField(min_length=8, widget=forms.PasswordInput, label="Введите пароль", )
    def __init__(self, *args, **kwargs):
        super(AuthorizeForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({'class' : 'form-control', 'placeholder':'Логин'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder':'Пароль'})

class ComputerForm(forms.ModelForm):
    class Meta:
        model = ComputerModel
        exclude = ['picpath']

    name = forms.CharField(label="Название")
    description = forms.CharField(label="Описание")
    file = forms.FileField(label="Выберите файл", allow_empty_file=True)
    def __init__(self, *args, **kwargs):
        super(ComputerForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class' : 'form-control', 'placeholder':'Название'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder':'Описание'})

class DateInput(forms.DateInput):
    input_type = "date"

class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderModel

        fields = ['date_completed']
        widgets = {
            'date_completed': DateInput()
        }
        labels = {
            'date_completed': "Введите дату исполнения заказа"
        }
