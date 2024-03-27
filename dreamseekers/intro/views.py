from django.conf import settings
from django.shortcuts import redirect, render

from .models import BusinessInfo, Contact, Instructors, Intro
from .forms import IntroForm,InstructorsForm

# 인사말
def greeting(request):

    instrs = Intro.objects.first()

    if request.method == 'POST':
        form = IntroForm(request.POST,instance=instrs)
        if form.is_valid():
            # 이미지가 등록되었다면
            if(request.POST.getlist('checkedImages')):
                # 기존에 등록된 이미지 삭제
                instrs.image.delete()
                # 새 이미지 추가
                instrs.image = request.FILES['image']

            form.save()
            return redirect('intro:greeting')
    else:
        form  = IntroForm(instance=instrs)
        intro = Intro.objects.first()
        
    return render(request, 'greeting.html', {'form':form,'intro':intro,})

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

# 강사 수정
def instrs_update(request,pk):
    # 관리자 여부 확인
    if not request.user.is_staff:
        return redirect('accounts:login')

    instrs = Instructors.objects.get(pk=pk)

    if request.method == 'POST':
        form = InstructorsForm(request.POST,instance=instrs)
        if form.is_valid():
            # 이미지가 등록되었다면
            if(request.POST.getlist('checkedImages')):
                # 기존에 등록된 이미지 삭제
                instrs.image.delete()
                # 새 이미지 추가
                instrs.image = request.FILES['image']

            form.save()
            return redirect('intro:instructors')
    return redirect('intro:instructors')

# 강사 삭제
def instrs_delete(request,pk):
    post = Instructors.objects.get(pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('intro:instructors')
    return render(request)

# 오시는 길
def contact(request):
    context = {'client_id': settings.NAVER_MAPS_CLIENT_ID}
    contacts = Contact.objects.first()
    business_info = BusinessInfo.objects.first()
    return render(request, 'contact.html', {'context':context, 'contacts':contacts, 'business_info':business_info,})