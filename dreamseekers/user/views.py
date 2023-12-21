from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from user.forms import UserForm

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid(): #유효성 검사
            user=User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password1'],
                email=request.POST['email'],
            )
            auth.login(request, user)
            return redirect('/')
        else: # 검사 실패시 form 전달
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserForm() # 빈 폼 생성
        return render(request, 'signup.html', {'form': form})

# 참고 #
# https://eveningdev.tistory.com/20
# https://wikidocs.net/72281