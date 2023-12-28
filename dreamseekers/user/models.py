from django.db import models

class User(models.Model):
    email = models.EmailField(verbose_name='이메일')
    password = models.CharField(max_length=64, verbose_name='비밀번호')
    created_dt = models.DateTimeField(auto_now=True, verbose_name='등록날짜')

    #객체를 문자열로 변환
    def __str__(self): 
        return self.email
    
    class Mata:
        db_table = 'my_user'
        verbose_name = '고객'
        verbose_name_plural = '고객'

