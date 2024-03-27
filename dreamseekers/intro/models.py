import datetime
import os
from django.db import models

class Intro(models.Model):
    title      = models.CharField(max_length=50, verbose_name='제목')
    contents   = models.TextField(max_length=3000, verbose_name='내용')
    image      = models.ImageField(upload_to='intro/intro/img/',blank=True, null=True, verbose_name='이미지')
    
    def __str__(self):
        return self.title
    
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

        super(Intro,self).delete(*args, **kargs)
    
    class Meta:
        db_table = "intro_Intro"
        verbose_name = "인사말"
        verbose_name_plural = "인사말"

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
    address              = models.CharField(max_length=100, verbose_name='주소1')
    sub_address          = models.CharField(max_length=100, verbose_name='주소2')
    weekday_start_time   = models.TimeField(default=datetime.time(9,0),verbose_name='평일시작시간')
    weekday_end_time     = models.TimeField(default=datetime.time(19,0),verbose_name='평일종료시간')
    weekend_start_time   = models.TimeField(default=datetime.time(9,0),verbose_name='주말시작시간')
    weekend_end_time     = models.TimeField(default=datetime.time(12,0),verbose_name='주말종료시간')
    phone                = models.CharField(max_length=20,verbose_name='연락처1')
    sub_phone            = models.CharField(max_length=20,verbose_name='연락처2')
    latitude             = models.FloatField(default=35.2220973957462,verbose_name='지도 위도')
    longitude            = models.FloatField(default=128.676299239476,verbose_name='지도 경도')
    map_add              = models.CharField(default="https://map.naver.com/p/entry/place/1605260808", max_length=100, verbose_name='지도 주소')

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