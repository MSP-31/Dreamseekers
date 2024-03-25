import os
from django.db import models

# 슬라이더 컨텐츠
class Slides(models.Model):
    title     = models.CharField(max_length=50, verbose_name='제목')
    contents  = models.TextField(max_length=3000, verbose_name='내용')
    image     = models.ImageField(upload_to='main/slide',blank=True, null=True, verbose_name='이미지')
    
    def __str__(self):
        return self.title
    
    # 이미지 삭제
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

        super(Slides,self).delete(*args, **kargs)
    
    class Meta:
        db_table = "main_slides"
        verbose_name = "메인 슬라이드"
        verbose_name_plural = "메인 슬라이드"