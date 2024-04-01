from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils import formats

from datetime import timedelta

from comment.forms import CommentForm
from comment.models import Comment
from comment.serializers import CommentSerializer

from user.models import Users
from .models import Post
from .forms import BoardForm

# 게시글 목록
def index(request):
    # 모든 Post를 불러오고 페이지에 가져옴
    post_list = Post.objects.order_by('-created_at')
    page = request.GET.get('page') # 페이지

    # 출력하는 Post수 제한
    paginator = Paginator(post_list,10)

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

# 게시글 자세히 보기
def post_detail(request, pk):
    # 게시글에서 pk(primary_key)로 해당 게시글 검색
    post = Post.objects.get(pk=pk)
    user_id = request.user.id

    # 모델 명
    board_name = "post"

    # 비밀글 확인
    if post.is_private:
        if (user_id == post.author.id) or (request.user.is_authenticated and request.user.is_staff):
            pass
        else:
            return HttpResponse('<script>alert("비밀글입니다. 접근 권한이 없습니다.");history.back();</script>')
    
    comments = Comment.objects.filter(postcommetns__post=post,parent=None)
    comment_form = CommentForm()

    # 댓글 직렬화
    serializer = CommentSerializer(comments, many=True)
    serialized_comments = serializer.data

    # 시간 차이 측정
    time_difference = post.updated_at - post.created_at
    show_updated_at = time_difference > timedelta(seconds=1)

    return render(request, 'post_detail.html',
                  {'post':post, 'comments':serialized_comments,'comment_form':comment_form,
                   'show_updated_at':show_updated_at,'board_name':board_name})

# 게시글 작성
def post_write(request):
    # 로그인 여부 확인
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/user/login/?next=' + request.META['HTTP_REFERER'])

    elif request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            user_id = request.user.id
            user = Users.objects.get(pk = user_id)

            # 비밀글 여부 확인
            is_private = request.POST.get('is_private', False) == 'on'

            new_post = Post.objects.create(
                title     = form.cleaned_data['title'],
                contents  = form.cleaned_data['contents'],
                is_private= is_private,
                author    = user
            )
            return redirect(post_detail,pk=new_post.pk)
        else:
            # 폼이 유효하지 않을 경우, 사용자가 입력한 데이터를 폼에 다시 채워 넣습니다.
            form = BoardForm(request.POST)
    else:
        form = BoardForm()
        
    return render(request, 'post_write.html', {'form':form})

# 게시글 수정
def post_update(request,pk):
    # 로그인 여부 확인
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/user/login/?next=' + request.META['HTTP_REFERER'])

    post = Post.objects.get(pk=pk)

    # 작성자가 아닌 경우 접근 불가
    if request.user != post.author:
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return redirect(post_detail, pk=post.pk)
    else:
        form = BoardForm(instance=post)
    return render(request, 'post_update.html', {'form': form, 'post': post})

# 게시글 삭제
def post_delete(request,pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('/board/guest/')
    return render(request, 'post_detail.html',{'post':post})

