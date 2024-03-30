from django.shortcuts import redirect, render

from .forms import SlidesForm

from .models import Slides

def main(request):
    slides = Slides.objects.all()

    return render(request, 'main.html',{'slides':slides})

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