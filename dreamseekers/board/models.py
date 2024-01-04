from django.db import models

class Post(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name='글쓴이')
    title = models.CharField(max_length=50, verbose_name='제목')
    contents = models.TextField(verbose_name='내용')
    created_dt = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    updated_dt = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    def __str__(self):
        return self.title