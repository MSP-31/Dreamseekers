from django.conf import settings
from django.shortcuts import redirect, render

from django.core import serializers

from intro.models import BusinessInfo, Contact

from .models import Slides
from lecture.models import lectureCalender, lectureTitle

from .forms import SlidesForm

def main(request):
    # 슬라이더
    slides = Slides.objects.all()
    # 주요강의
    lectureTitles = lectureTitle.objects.all()

    # 캘린더
    # DB에서 이벤트 데이터 가져오기
    schedules = lectureCalender.objects.all()
    schedules_json = serializers.serialize('json', schedules)

    # 오시는길
    context = {'client_id': settings.NAVER_MAPS_CLIENT_ID}
    contacts = Contact.objects.first()
    business_info = BusinessInfo.objects.first()

    return render(request, 'main.html',{'slides':slides,'lectures':lectureTitles,'schedules': schedules_json,
                                        'context':context, 'contacts':contacts, 'business_info':business_info,})

# 메인슬라이더
def slide_modify(request):
    # 관리자 여부 확인
    if not request.user.is_staff:
        return redirect('accounts:login')
    
    slideList = Slides.objects.all()
    form = SlidesForm()

    if request.method == 'POST':
        form = SlidesForm(request.POST, request.FILES)

        if form.is_valid():
            new_slides = Slides.objects.create(
                title     = form.cleaned_data['title'],
                contents  = form.cleaned_data['contents'],
                image     = request.FILES.get('image'),
            )
            return redirect('slide_modify')
    return render(request, 'slide_modify.html',{'form': form,'titles':slideList})

# 메인슬라이더 수정
def slide_update(request,pk):
    # 관리자 여부 확인
    if not request.user.is_staff:
        return redirect('accounts:login')

    slide = Slides.objects.get(pk=pk)

    if request.method == 'POST':
        form = SlidesForm(request.POST,instance=slide)
        if form.is_valid():
            # 이미지가 등록되었다면
            if(request.POST.getlist('checkedImages')):
                # 기존에 등록된 이미지 삭제
                slide.image.delete()
                # 새 이미지 추가
                slide.image = request.FILES['image']

            form.save()
    return redirect('slide_modify')

# 메인슬라이더 삭제
def slide_del(request,pk):
    slide = Slides.objects.get(pk=pk)

    if request.method == 'POST':
        slide.delete()
        return redirect('slide_modify')
    return render(request)

# 개인정보처리방침
def privacy_policy(request):
    return render(request, 'privacy_policy.html')

# 이메일 무단수집 거부
def unauthorized_collection(request):
    return render(request, 'unauthorized_collection.html')