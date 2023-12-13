from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

#https://eveningdev.tistory.com/20 참고

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            USER = User.objects.create_user( #새 유저객체 생성
                email=request.POST['email'],
                password=request.POST['password1'],
                username=request.POST['username'],
            )
            auth.login(request, USER)
            return redirect('/')
        return render(request,'signup.html')
    return render(request, 'signup.html')
        