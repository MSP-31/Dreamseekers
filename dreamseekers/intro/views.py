from django.conf import settings
from django.shortcuts import redirect, render

from .models import Instructors
from .forms import InstructorsForm

# 인사말
def greeting(request):
    return render(request, 'greeting.html')

# 강사 소개
def instructors(request):
    if request.method == 'POST':
        form = InstructorsForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = Instructors.objects.create(
                name      = form.cleaned_data['name'],
                contents  = form.cleaned_data['contents'],
                image     = request.FILES.get('image'),
            )
            return redirect('intro:instructors')
    else:
        form = InstructorsForm()
        list = Instructors.objects.order_by()
        
    return render(request, 'instructors.html', {'form':form, 'list':list,})

# 게시글 삭제
def instrs_delete(request,pk):
    post = Instructors.objects.get(pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('intro:instructors')
    
    form = InstructorsForm()
    list = Instructors.objects.order_by()
    return render(request, 'instructors.html', {'form':form, 'list':list,})

# 오시는 길
def contact(request):
    context = {'client_id': settings.NAVER_MAPS_CLIENT_ID}
    return render(request, 'contact.html',context)