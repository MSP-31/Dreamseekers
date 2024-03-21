from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from .models import Users

class LoginForm(forms.Form):
    username = forms.CharField(
        error_messages={'required' : '아이디를 입력해주세요'},
        max_length=32, label='아이디')
    password = forms.CharField(
        error_messages={'required' : '비밀번호를 입력해주세요.'},
        max_length=64, label='비밀번호', widget=forms.PasswordInput)
    
    def clean(self):
        cleand_data = super().clean()
        username = cleand_data.get('username')
        password = cleand_data.get('password')

        if password and username:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError('아이디 또는 비밀번호가 일치하지 않습니다.')

class SignUpForm(forms.Form):
    username = forms.CharField(label='아이디')
    password = forms.CharField(
        widget=forms.PasswordInput,label='비밀번호')
    re_password = forms.CharField(
        widget=forms.PasswordInput,label='비밀번호 확인')
    email = forms.EmailField(
        widget=forms.EmailInput,label='이메일')

    # 유저이름 검사
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Users.objects.filter(username=username).exists():
            raise forms.ValidationError('이미 존재하는 id 입니다.')
        return username

    # 비밀번호 유효성 검사
    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password and re_password and password != re_password:
            raise forms.ValidationError('2차 비밀번호가 다릅니다.')
        return re_password

    # 이메일 중복 검사
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Users.objects.filter(email=email).exists():
            raise forms.ValidationError('이미 존재하는 이메일입니다.')
        return email