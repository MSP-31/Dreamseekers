from django.db import models

# 게시글
class Post(models.Model):
    author     = models.ForeignKey('user.Users', on_delete=models.CASCADE,related_name='board_posts', verbose_name='글쓴이')
    title      = models.CharField(max_length=50, verbose_name='제목')
    contents   = models.TextField(max_length=3000, verbose_name='내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='수정일')
    is_private = models.BooleanField(default=False, verbose_name='비밀글')
    
    def __str__(self):
        return self.title
    
    # 저장
    def save(self, *args, **kwargs):
        super(Post, self).save()

    
    # 게시글 삭제
    def delete(self, *args, **kargs):
        super(Post,self).delete(*args, **kargs)
    
    class Meta:
        db_table = "community_board"
        verbose_name = "게시물"
        verbose_name_plural = "게시물"