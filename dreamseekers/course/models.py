from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=256, verbose_name='강의명')
    description = models.TextField(verbose_name='강의설명')
    image = models.ImageField(upload_to='course', null=True ,verbose_name='강의사진')
    created_dt = models.DateTimeField(auto_now_add='True', verbose_name='등록날짜')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'courseList' 
        verbose_name = '강의'
        verbose_name_plural = '강의'