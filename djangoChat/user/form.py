from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name', 'password1', 'password2']

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Tên đăng nhập'
        self.fields['password1'].label = 'Mật khẩu'
        self.fields['password2'].label = 'Nhập lại mật khẩu'
        self.fields['first_name'].label = 'Họ'
        self.fields['last_name'].label = 'Tên'

        self.fields['username'].help_text = 'Yêu cầu dưới 150 ký tự, chỉ chứa chữ cái, số và @/./+/-/_'
        self.fields['email'].help_text = 'Yêu cầu dưới 254 ký tự, phải chứa @'
        self.fields['password2'].help_text = 'Nhập lại mật khẩu của bạn'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exists')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user