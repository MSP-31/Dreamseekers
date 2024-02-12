from django.db import models
from django.core.validators import RegexValidator

class Users(models.Model):
    phoneNumberRegex = RegexValidator(regex = r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')

    username   = models.CharField(unique=True, max_length=100, verbose_name='id')
    email      = models.EmailField(unique=True, verbose_name='이메일')
    password   = models.CharField(max_length=300, verbose_name='비밀번호')
    phone      = models.CharField(validators=[phoneNumberRegex], max_length=11, verbose_name='전화번호')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    
    def __str__(self): 
        return self.username
    
    class Meta:
        verbose_name = '유저'
        verbose_name_plural = '유저'