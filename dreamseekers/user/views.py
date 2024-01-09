from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
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
        errorMsg = {}
        
        # 비밀번호/이메일 유효성 검사
        if not is_valid_password(password):
            errorMsg['password'] = '비밀번호는 8자 이상, 숫자, 영문 대/소문자, 특수문자를 포함해야 합니다.'

        if not (username and email and password and repassword):
            errorMsg['error'] = "모든 값을 입력해야 합니다."

        elif password != repassword:
            errorMsg['error'] = "비밀번호가 다릅니다."
        else:
            print(password)
            user = Users(
                username = username,
                password = make_password(password),
                email = email
            )
            user.save()
            return redirect('/')
    return render(request,'signup.html',errorMsg)
# 참고
# https://iamthejiheee.tistory.com/57

# 비밀번호 유효성 검사
def is_valid_password(password):
    
    # 비밀번호 길이 검사
    if len(password) < 8:
        return False
    
    # 숫자, 대소문자, 특수문자 포함 검사
    for char in password:
        if not char.isalnum() and not char in ['!', '@', '#', '$', '%', '&', '*', '(', ')', '-', '_', '+', '=', ',', '.', '/', '\\']:
            return False
    return True

# 이메일 중복 검사
def is_valid_email(email):
    return True

# 로그인
def login(request):
    if request.method == 'GET':
        form = LoginForm()
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.user_id
            request.session['username'] = form.user_name
            return redirect('/')
    return render(request, 'login.html', {'form':form})

# 로그아웃
def logout(request):
    if request.session.get('user'):
        del(request.session['user'])
    return redirect('/')