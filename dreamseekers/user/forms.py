from django import forms
from .models import Users
from django.contrib.auth.hashers import check_password

class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={"required" : "이메일을 입력해주세요"},
                               max_length=32, label="이메일")
    password = forms.CharField(error_messages={"required" : "비밀번호를 입력해주세요."},
                               max_length=64, label="비밀번호", widget=forms.PasswordInput)
    
    def clean(self):
        cleand_data = super().clean()
        email = cleand_data.get('email')
        password = cleand_data.get('password')

        if password and email:
            try:
                user = Users.objects.get(email=email)
            except Users.DoesNotExist:
                self.add_error("email","이메일이 존재하지 않습니다.")
                return
            if not check_password(password,user.password):
                self.add_error("password", "비밀번호가 일치하지 않습니다.")
            else:
                self.user_id = user.id

