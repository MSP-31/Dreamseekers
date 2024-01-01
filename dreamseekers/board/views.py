from django.shortcuts import render
from .models import Post

def index(request):
    # 모든 Post를 불러오고 페이지에 가져옴
    postlist = Post.objects.all()
    return render(request, 'index.html',{'postlist':postlist})

def posting(request, pk):
    # 게시글에서 pk(primary_key)로 해당 게시글 검색
    post = Post.objects.get(pk=pk)
    return render(request, 'post.html',{'post':post})