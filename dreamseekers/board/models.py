import os
from django.conf import settings
from django.db import models

# 파일 업로드 경로
def upload_path(post, filename):
    return f'board/img/{post.pk}/{filename}'

# 게시글
class Post(models.Model):
    author     = models.ForeignKey('user.Users', on_delete=models.CASCADE, verbose_name='글쓴이')
    title      = models.CharField(max_length=50, verbose_name='제목')
    contents   = models.TextField(max_length=3000, verbose_name='내용')
    photo      = models.ImageField(upload_to=upload_path, blank=True, null=True, verbose_name='이미지')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='수정일')
    is_private = models.BooleanField(default=False, verbose_name='비밀글')
    
    def __str__(self):
        return self.title
    
    # 게시글이 삭제되면 이미지도 같이 삭제
    def delete(self, *args, **kargs):
        if self.photo:
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT, 'board/images/{}/'.format(self.pk), self.photo.path))
            except FileNotFoundError:
                pass
        else: #이미지 파일이 없는 경우
            pass
        super(Post,self).delete(*args, **kargs)
    
    class Meta:
        db_table = "community_board"
        verbose_name = "게시물"
        verbose_name_plural = "게시물"

# 댓글
class Comment(models.Model):
    article = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey('user.Users',on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__ (self):
        return self.content
    
    class Meta:
        db_table = "community_comment"
        verbose_name = "댓글"
        verbose_name_plural = "댓글"