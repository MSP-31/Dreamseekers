from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout
from django.contrib.auth.backends import ModelBackend

from .models import Users
from .forms import LoginForm, SignUpForm

# 회원가입
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = Users(
                username = form.cleaned_data['username'],
                password = make_password(form.cleaned_data['password']),
                email    = form.cleaned_data['email'],
            )
            user.save()

            # 바로 로그인
            backend = ModelBackend()
            user.backend = f'{backend.__module__}.{backend.__class__.__name__}'
            login(request,user)

            return redirect('/')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

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