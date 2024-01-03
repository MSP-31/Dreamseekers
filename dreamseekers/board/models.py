from django.db import models

class Post(models.Model):
    postname = models.CharField(max_length=50, verbose_name='제목')
    contents = models.TextField(verbose_name='내용')
    created_dt = models.DateTimeField(auto_now=True, verbose_name='등록날짜')

    def __str__(self):
        return self.postname