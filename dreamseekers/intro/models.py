import os
from django.db import models

# 강사 소개
class Instructors(models.Model):
    name       = models.CharField(max_length=50, verbose_name='이름')
    contents   = models.TextField(max_length=3000, verbose_name='내용')
    image      = models.ImageField(upload_to='intro/instrs/img/',blank=True, null=True, verbose_name='이미지')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    
    def __str__(self):
        return self.name
    
    # 강사진 삭제
    def delete(self, *args, **kargs):

        # 이미지가 존재하면 같이 삭제
        if self.image:
            if os.path.isfile(self.image.path):
                try:
                    # 이미지 삭제
                    os.remove(self.image.path)
                except FileNotFoundError:
                    pass
            else: #이미지 파일이 없는 경우
                pass
            self.image.delete()

        super(Instructors,self).delete(*args, **kargs)
    
    class Meta:
        db_table = "intro_Instructors"
        verbose_name = "강사진"
        verbose_name_plural = "강사진"
    