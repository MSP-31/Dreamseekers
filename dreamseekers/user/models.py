from django.db import models

class Users(models.Model):
    username   = models.CharField(max_length=100, verbose_name='이름')
    email      = models.EmailField(unique=True, verbose_name='이메일')
    password   = models.CharField(max_length=300, verbose_name='비밀번호')
    created_dt = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    updated_dt = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    # 익명사용자 x
    @property
    def is_anonymous(self):
        return False
    
    @property
    def is_authenticated(self):
        return True
    
    def __str__(self): 
        return self.username