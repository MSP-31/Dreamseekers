import re
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout
from django.contrib.auth.backends import ModelBackend

from .models import Users
from .forms import LoginForm

# 회원가입
def signup(request):
    if request.method == 'GET':
        return render(request,'signup.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('re-password', None)
        email = request.POST.get('email', None)

        errorMsg = error_form(username,password,repassword,email)

        if errorMsg:
            return render(request,'signup.html',errorMsg)
        
        else:
            user = Users(
                username = username,
                password = make_password(password),
                email = email,
            )
            user.save()

            # 바로 로그인
            backend = ModelBackend()
            user.backend = f'{backend.__module__}.{backend.__class__.__name__}'
            login(request,user)

            return redirect('/')
    return render(request,'signup.html',errorMsg)

# 로그인
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request,form.user)
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form})

# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('/')

# 유효성 검사 폼
def error_form(username, password, repassword, email):
    errorMsg = {}

    if not (username and email and password and repassword):
        errorMsg['error'] = '모든 값을 입력해야 합니다.'
    
    username_error = is_valid_username(username)
    if username_error:
        errorMsg['username'] = username_error

    password_error = is_valid_password(password, repassword)
    if password_error:
        errorMsg['password'] = password_error

    emaill_error = is_valid_email(email)
    if emaill_error:
        errorMsg['emaill_error'] = emaill_error

    return errorMsg

# 유저이름 검사
def is_valid_username(username):
    if Users.objects.filter(username=username).exists():
        return '이미 존재하는 id 입니다.'
    return None

# 비밀번호 유효성 검사
def is_valid_password(password,repassword):
    
    # 비밀번호 길이 검사
    if len(password) < 8:
        return '비밀번호는 8자 이상이어야 합니다.'
    
    # 비밀번호 확인
    elif password != repassword:
        return '2차 비밀번호가 다릅니다.'
    
    # 숫자, 대소문자, 특수문자 포함 검사
    for char in password:
        if not char.isalnum() and not char in ['!', '@', '#', '$', '%', '&', '*', '(', ')', '-', '_', '+', '=', ',', '.', '/', '\\']:
            return '비밀번호는 숫자, 영문 대/소문자, 특수문자를 포함해야 합니다.'
    return None

# 이메일 중복 검사
def is_valid_email(email):
    if Users.objects.filter(email=email).exists():
        return '이미 존재하는 이메일입니다.'
    return None