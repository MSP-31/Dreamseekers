from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout
from django.contrib.auth.backends import ModelBackend

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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
            
            # 만약에 이전 페이지가 존재한다면
            next_url = request.POST.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)
            return redirect('/')
            
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form})

# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('/')

# 계정 관리
def account(request):
    return render(request,'account.html')

# 계정 수정
def account_modify(request):
    # 현재 로그인되어있는 계정
    user = request.user

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        user_account = Users.objects.get(pk=user.id)
        if form.is_valid():
            user_account.username = form.cleaned_data['username'],
            user_account.password = make_password(form.cleaned_data['password']),
            user_account.email    = form.cleaned_data['email'],
            user_account.save()

            return redirect('accounts:account')
    else:
        initial_data = {'username': user.username, 'email': user.email}
        form = SignUpForm(initial=initial_data)

    return render(request,'account_modify.html',{'form': form})

# 계정탈퇴
def account_del(request):
    user = Users.objects.get(pk=request.user.id)
    user.delete()
    return redirect('/')

# 이메일 보내기
def send_email(title, message,pk):
    html_message = render_to_string("smtp_email.html",{'title':title ,'message': message, 'id': pk})
    plain_message = strip_tags(html_message)  # HTML 태그 제거
    subject = '새로운 강의 상담 문의'
    email = settings.EMAIL
    send_mail(subject, plain_message, email, [email], html_message=html_message)