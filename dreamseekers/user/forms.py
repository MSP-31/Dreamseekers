from django import forms
from django.contrib.auth import authenticate

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
