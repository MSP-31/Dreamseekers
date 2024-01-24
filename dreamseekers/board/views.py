import os
from django.conf import settings
from django.http import Http404

from django.shortcuts import get_object_or_404, redirect, render
from user.models import Users
from .models import Comment, Post
from .forms import BoardForm, CommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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

#게시글 자세히 보기
def post_detail(request, pk):
    # 게시글에서 pk(primary_key)로 해당 게시글 검색
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(article=pk)
    comment_form = CommentForm()
    
    user_id = request.session.get('user')

    # 비밀글 확인
    if post.is_private:
        if (user_id == post.author.id) or request.user.is_authenticated and (request.user.is_staff):
            pass
        else:
            raise Http404('비밀글입니다.')
    return render(request, 'post_detail.html',{'post':post, 'comments':comments, 'comment_form':comment_form,})

# 게시글 작성
def post_write(request):
    # 로그인 여부 확인
    if not request.session.get('user'):
        return redirect('accounts:login')

    elif request.method == 'POST':
        form = BoardForm(request.POST,request.FILES)
        if form.is_valid():
            user_id = request.session.get('user')
            user = Users.objects.get(pk = user_id)

            new_post = Post.objects.create(
                title     = form.cleaned_data['title'],
                contents  = form.cleaned_data['contents'],
                photo     = form.cleaned_data['photo'],
                is_private= form.cleaned_data['is_private'],
                author    = user
            )

            new_post.save()
            return redirect(post_detail,pk=new_post.pk)
        else:
            # 폼이 유효하지 않을 경우, 사용자가 입력한 데이터를 폼에 다시 채워 넣습니다.
            form = BoardForm(request.POST)
    else:
        form = BoardForm()
        
    return render(request, 'post_write.html', {'form':form})

# 게시글 수정
def post_update(request,pk):
    post = Post.objects.get(pk=pk)
    original_photo = post.photo

    if request.method == 'POST':
        form = BoardForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            # 이미지를 삭제
            if(original_photo == ""):
                pass
            # 이미지를 수정
            elif original_photo != post.photo:
                os.remove(os.path.join(settings.MEDIA_ROOT, 'board/images/{}/'.format(post.pk), original_photo.path))
            form.save()
            return redirect(post_detail,pk=post.pk)
        else:
            # 폼이 유효하지 않을 경우, 사용자가 입력한 데이터를 폼에 다시 채워 넣습니다.
            form = BoardForm(request.POST)
        return redirect('/board')
    else:
        form = BoardForm(instance=post)
    return render(request, 'post_update.html', {'form': form, 'post': post})

# 게시글 삭제
def post_delete(request,pk):
    post = Post.objects.get(pk=pk)
    print(request.method)
    if request.method == 'POST':
        post.delete()
        return redirect('/board')
    return render(request, 'post_detail.html',{'post':post})

# 댓글 작성
def comments_create(request,pk):
    if request.session.get('user'):
        article = get_object_or_404(Post, pk=pk)
        comment_form = CommentForm(request.POST)

        user_id = request.session.get('user')
        user = Users.objects.get(pk = user_id)
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = user
            comment.save()
        return redirect('post_detail',article.pk)
    return redirect('accounts:login')

# 댓글 수정
def comments_update(request, post_pk, comment_pk):
    if request.session.get('user'):
        comments = Comment.objects.get(pk=comment_pk)
        comment_form = CommentForm(instance = comments)
        print("야호")
        if request.method == "POST":
            update_form = CommentForm(request.POST,instance = comments)
            print("야야")
            update_form.save()
            return redirect('post_detail',post_pk)
    return render(request,'comments_update.html',{'comment_form':comment_form})

# 댓글 삭제
def comments_delete(request, post_pk ,comment_pk):
    if request.session.get('user'):
        comment = get_object_or_404(Comment,pk=comment_pk)
        if request.session.get('user') == comment.user.id:
            comment.delete()
    return redirect('post_detail',post_pk)