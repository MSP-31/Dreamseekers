from django import forms
from .models import Users
from django.contrib.auth.hashers import check_password

class LoginForm(forms.Form):
    username = forms.CharField(error_messages={"required" : "아이디를 입력해주세요"},
                               max_length=32, label="아이디")
    password = forms.CharField(error_messages={"required" : "비밀번호를 입력해주세요."},
                               max_length=64, label="비밀번호", widget=forms.PasswordInput)
    
    def clean(self):
        cleand_data = super().clean()
        username = cleand_data.get('username')
        password = cleand_data.get('password')

        if password and username:
            try:
                user = Users.objects.get(username=username)
            except Users.DoesNotExist:
                self.add_error("username","아이디가 존재하지 않습니다.")
                return
            if not check_password(password,user.password):
                self.add_error("password", "비밀번호가 일치하지 않습니다.")
            else:
                self.user_id = user.id
                self.user_name = user.username
