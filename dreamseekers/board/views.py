from django.shortcuts import redirect, render
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def index(request):
    # 모든 Post를 불러오고 페이지에 가져옴
    post_list = Post.objects.order_by('-created_dt')
    page = request.GET.get('page') # 페이지

    # 출력하는 Post수 제한
    paginator = Paginator(post_list,5)

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

    return render(request, 'index.html',{'page_obj':page_obj, 'paginator':paginator, 'custom_range':custom_range})

def posting(request, pk):
    # 게시글에서 pk(primary_key)로 해당 게시글 검색
    post = Post.objects.get(pk=pk)
    return render(request, 'post.html',{'post':post})

# 글쓰기
def write(request):
    # 로그인 여부 확인
    if not request.session.get('user'):
        return redirect('/user/login')

    if request.method == 'POST':
        print("ㅡㅡㅡ시작ㅡㅡㅡㅡ")
        print(request.POST['title'])
        print(request.POST['contents'])
        print("ㅡㅡㅡ끝ㅡㅡㅡㅡ")
        if title and contents:  # title과 contents가 모두 존재하는지 확인
            new_post=Post.objects.create(
                title=request.POST['title'],
                contents=request.POST['contents'],
            )
        return redirect('/')
    return render(request,'write.html')