import os
from django.db import models

# 강사 소개
class Instructors(models.Model):
    name       = models.CharField(max_length=50, verbose_name='이름')
    contents   = models.TextField(max_length=3000, verbose_name='내용')
    image      = models.ImageField(upload_to='intro/instrs/img/',blank=True, null=True, verbose_name='이미지')
    
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

# 오시는 길
class Contact(models.Model):
    address     = models.CharField(max_length=100, verbose_name='주소1')
    sub_address = models.CharField(max_length=100, verbose_name='주소2')
    startTime   = models.TimeField(verbose_name='시작시간')
    endTime     = models.TimeField(verbose_name='종료시간')
    phone       = models.CharField(max_length=20,verbose_name='연락처1')
    sub_phone   = models.CharField(max_length=20,verbose_name='연락처2')

    def __str__(self):
        return self.address

    class Meta:
        db_table = "intro_Contact"
        verbose_name = "오시는 길"
        verbose_name_plural = "오시는 길"

# 사업자 정보
class BusinessInfo(models.Model):
    rep       = models.CharField(max_length=50, verbose_name='대표자')
    email     = models.EmailField(verbose_name='이메일')
    CRN       = models.CharField(max_length=50, verbose_name='사업자등록번호')
    depositor = models.CharField(max_length=50, verbose_name='예금주')
    bank      = models.CharField(max_length=50, verbose_name='입금은행')
    account   = models.CharField(max_length=50, verbose_name='계좌번호')

    def __str__(self):
        return self.rep

    class Meta:
        db_table = "intro_BusinessInfo"
        verbose_name = "사업자 정보"
        verbose_name_plural = "사업자 정보"