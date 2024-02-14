from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from user.models import Users
from .models import Comment, PostCommetns
from .forms import CommentForm

# 댓글 작성
def comments_create(request,pk,board_name):
    if request.session.get('user'):
        # 해당 모델 찾기
        content_type = ContentType.objects.get(model=board_name)
        ModelClass = content_type.model_class()
        # 찾은 모델로 검색
        post = ModelClass.objects.get(pk=pk)
        
        comment_form = CommentForm(request.POST)

        user_id = request.session.get('user')
        user = Users.objects.get(pk = user_id)
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = user
            comment.save()

            # PostComments에 저장 / setattr 함수로 유동적으로 저장
            post_comment = PostCommetns(comment=comment)
            setattr(post_comment, board_name, post)
            post_comment.save()

        if board_name == 'post':
            return redirect('post_detail', post.pk)
        else:
            return redirect('inquiry:inquiry_detail', post.pk)
    return redirect('accounts:login')

# 댓글 수정
def comments_update(request, post_pk, comment_pk):
    if request.session.get('user'):
        comments = Comment.objects.get(pk=comment_pk)
        comment_form = CommentForm(instance = comments)
        if request.method == "POST":
            update_form = CommentForm(request.POST,instance = comments)
            update_form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            #return redirect('post_detail',post_pk)
    return render(request,'comments_update.html',{'comment_form':comment_form})

# 댓글 삭제
def comments_delete(request, comment_pk):
    if request.session.get('user'):
        comment = get_object_or_404(Comment,pk=comment_pk)
        if request.session.get('user') == comment.user.id:
            comment.delete()
    # 삭제후 이전 페이지로 돌아감
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# 대댓글 작성
def comments_nested(request, post_pk, comment_pk, board_name):
    if request.session.get('user'):
        # 해당 모델 찾기
        content_type = ContentType.objects.get(model=board_name)
        ModelClass = content_type.model_class()
        # 찾은 모델로 검색
        post = ModelClass.objects.get(pk=post_pk)

        comment_form = CommentForm(request.POST)

        user_id = request.session.get('user')
        user = Users.objects.get(pk = user_id)

        # 부모 댓글 여부
        comments = Comment.objects.get(pk=comment_pk)
        parents = comments.parent
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = user
            # 부모 댓글값이 없다면 새로 추가
            if parents is None:
                comment.parent = comments
            # 부모 댓글값이 있다면 상속
            else:
                comment.parent = parents
            comment.save()
            
        if board_name == 'post':
            return redirect('post_detail', post.pk)
        else:
            return redirect('inquiry:inquiry_detail', post.pk)
    return redirect('accounts:login')