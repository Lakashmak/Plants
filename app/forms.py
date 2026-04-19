from django import forms
from django.contrib.auth.forms import UserCreationForm
import re
from django.db.models import Q
import hashlib
from .models import User

class ContactForm(forms.Form): # placeholder
    name = forms.CharField(label='ФИО', max_length=100) # , required=False
    phone = forms.CharField(label='телефон', max_length=12)
    email = forms.EmailField(label='email')
    address = forms.CharField(widget=forms.Textarea, label='адрес доставки')
    password = forms.CharField(label='придумайте пароль', max_length=100)
    repassword = forms.CharField(label='повторите пароль', max_length=100)
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('gmail.com'):
            raise forms.ValidationError("Электронная почта должна иметь домен gmail.com")
        elif User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким адресом электронной почты уже существует!")
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password') # cleaned_data = super().clean()
        repassword = self.cleaned_data.get('repassword')
        if password and repassword and password != repassword:
            raise forms.ValidationError("Пароли не совпадают!") # self.add_error('password', "Пароли не совпадают!\n" + password + "\n" + repassword)
        return password
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.match(r'^\+?[1-9]\d{1,14}$', phone):
            raise forms.ValidationError("Введите корректный номер телефона!")
        elif User.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError("Пользователь с таким номером телефона уже существует!")
        return phone
    
    # class Meta(UserCreationForm.Meta):
    #     fields = ("name", "phone", "email", "address", "password", "repassword")

class LoginForm(forms.Form):
    login = forms.CharField(label='логин', max_length=100)
    password = forms.CharField(label='пароль', max_length=100)

    def clean(self):
        cleaned_data = super().clean()
        login = self.cleaned_data.get('login')
        password = self.cleaned_data.get('password')
        if not User.objects.filter(Q(phone_number=login) | Q(email=login)).exists():
            raise forms.ValidationError("Пользователь не найден!")
        else:
            password_hash1 = User.objects.filter(Q(phone_number=login) | Q(email=login)).values('password_hash').first()['password_hash']
            password_hash2 = hashlib.sha256(str(password).strip().encode()).hexdigest()
            if password_hash1 and password_hash2 and password_hash1 != password_hash2:
                raise forms.ValidationError("Неверный пароль!\n" + password_hash1 + "\n" + password_hash2)
        return cleaned_data

