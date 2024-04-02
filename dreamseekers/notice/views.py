from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from datetime import timedelta

from user.models import Users
from .models import File, Image, Notice
from .forms import NoticeForm

from django.views.generic import ListView
from django.contrib import messages
from django.db.models import Q

# 페이지당 항목 수
ITEMS_PER_PAGE = 10

# 게시글 목록
def index(request):
    # 모든 Notice를 불러오고 페이지에 가져옴
    list = Notice.objects.order_by('-created_at')
    page = request.GET.get('page') # 페이지

    # 출력하는 Notice수 제한
    paginator = Paginator(list,ITEMS_PER_PAGE)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger: # 페이지가 지정되지 않았을때
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage: # 페이지 범위를 초과할때
        page = paginator.num_pages
        page_obj = paginator.page(page)

    leftIndex = (int(page) -5)
    if leftIndex <1:
        leftIndex = 1
    rightIndex = (int(page) +5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages

    custom_range = range(leftIndex, rightIndex+1)

    return render(request, 'notice_index.html',{'page_obj':page_obj, 'paginator':paginator, 'custom_range':custom_range})

# 게시글 자세히 보기
def detail(request, pk):
    # 게시글에서 pk(primary_key)로 해당 게시글 검색
    post = Notice.objects.get(pk=pk)

    # 시간 차이 측정
    time_difference = post.updated_at - post.created_at
    show_updated_at = time_difference > timedelta(seconds=1)

    return render(request, 'notice_detail.html',{'post':post,'show_updated_at':show_updated_at,})

# 게시글 작성
def write(request):
    # 로그인 여부 확인
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/user/login/?next=' + request.META['HTTP_REFERER'])

    elif request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            user_id = request.user.id
            user = Users.objects.get(pk = user_id)

            new_post = Notice.objects.create(
                title     = form.cleaned_data['title'],
                contents  = form.cleaned_data['contents'],
                author    = user
            )
            # 여러개의 이미지 처리
            for image in request.FILES.getlist('image'):
                image = Image.objects.create(image=image)
                new_post.image.add(image)

            # 여러개의 파일 처리
            for file in request.FILES.getlist('files'):
                files = File.objects.create(file=file)
                new_post.files.add(files)
            
            new_post.save()

            return redirect('notice:detail',pk=new_post.pk)
        else:
            # 폼이 유효하지 않을 경우, 사용자가 입력한 데이터를 폼에 다시 채워 넣습니다.
            form = NoticeForm(request.POST)
    else:
        form = NoticeForm()
        
    return render(request, 'notice_write.html', {'form':form})

# 게시글 수정
def update(request,pk):
    # 로그인 여부 확인
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/user/login/?next=' + request.META['HTTP_REFERER'])

    post = Notice.objects.get(pk=pk)

    # 작성자가 아닌 경우 접근 불가
    if request.user != post.author:
        return redirect('notice:detail', pk=pk)
    
    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=post)
        if form.is_valid():
            print(request.POST.getlist('checkedImages'))
            # 기존 이미지 삭제
            for image in Image.objects.filter(notice=post):
                if 'deleteImage' + str(image.id) in request.POST:
                    image.delete()
            # 기존 파일 삭제
            for file in File.objects.filter(notice=post):
                if 'deleteFile' + str(file.id) in request.POST:
                    file.delete()

            # 새 이미지 추가
            for image in request.FILES.getlist('image'):
                image = Image.objects.create(image=image)
                post.image.add(image)
            
            # 새 파일 추가
            for file in request.FILES.getlist('files'):
                files = File.objects.create(file=file)
                post.files.add(files)

            post.save()
            return redirect('notice:detail', pk=post.pk)
        
    else:
        form = NoticeForm(instance=post)
    return render(request, 'notice_update.html', {'form': form, 'post': post})

# 게시글 삭제
def delete(request,pk):
    post = Notice.objects.get(pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('notice:index')
    return render(request, 'notice_detail.html',{'post':post})

# 게시글 검색 기능
class NoticeView(ListView):
    model = Notice  # 모델 설정
    template_name = 'notice_index.html'  # 템플릿 이름 설정

    # 기본 쿼리셋 지정
    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        notice_list = Notice.objects.order_by('-id')

        if search_keyword:
            if len(search_keyword) > 1:
                if search_type == 'all':
                    search_notice_list = notice_list.filter(Q (title__icontains=search_keyword) | Q (contents__icontains=search_keyword))
                elif search_type == 'title':
                    search_notice_list = notice_list.filter(title__icontains=search_keyword)    
                elif search_type == 'contents':
                    search_notice_list = notice_list.filter(contents__icontains=search_keyword)
                return search_notice_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return notice_list
    
    # 템플릿에 전달될 컨텍스트 데이터 지정
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_keyword = self.request.GET.get('q', '')

        if len(search_keyword) > 1:
            context['q'] = search_keyword

        # notice_list에 쿼리셋 할당
        notice_list = self.get_queryset()

        # Paginator 객체 생성
        paginator = Paginator(notice_list, ITEMS_PER_PAGE)
        
        # 현재 페이지 번호 가져옴
        page_number = self.request.GET.get('page')

        # Page 객체 생성
        page_obj = paginator.get_page(page_number)

        # page_obj를 컨텍스트에 추가
        context['page_obj'] = page_obj

        return context