from django.db import models

class User(models.Model):
    user_id     = models.CharField(max_length=100, verbose_name='id')
    email       = models.EmailField(verbose_name='이메일')
    password    = models.CharField(max_length=64, verbose_name='비밀번호')
    created_dt = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    updated_dt = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    def __str__(self): 
        return self.user_id

