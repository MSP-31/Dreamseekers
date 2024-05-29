import os
from django.db import models

# 상담 문의
class Inquiry(models.Model):
    author     = models.ForeignKey('user.Users', on_delete=models.CASCADE, related_name='lecture_posts', verbose_name='글쓴이')
    phone      = models.CharField(max_length=45, verbose_name='연락처')
    title      = models.CharField(max_length=50, verbose_name='제목')
    contents   = models.TextField(max_length=3000, verbose_name='내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "lecture_inquiry"
        verbose_name = "강의상담문의"
        verbose_name_plural = "강의상담문의"

# 강의 일정
class lectureCalender(models.Model):
    contents   = models.CharField(max_length=50, verbose_name='내용')
    date       = models.DateField(verbose_name='날짜')
    startTime  = models.TimeField(verbose_name='시작시간')
    endTime    = models.TimeField(verbose_name='종료시간')
    allDay     = models.BooleanField(default = False, verbose_name='종일')

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')
    
    # 게시글 삭제
    def delete(self, *args, **kargs):
        super(lectureCalender,self).delete(*args, **kargs)
    
    class Meta:
        db_table = "lecture_calender"
        verbose_name = "강의일정"
        verbose_name_plural = "강의일정"

# 주요강의
class lectureTitle(models.Model):
    title    = models.CharField(max_length=50, verbose_name='제목')
    contents = models.TextField(max_length=200, verbose_name='설명')
    image    = models.ImageField(upload_to='lecture/list/img/',blank=True, null=True, verbose_name='이미지')

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

        super(lectureTitle,self).delete(*args, **kargs)
    
    class Meta:
        db_table = "lecture_title"
        verbose_name = "강의제목"
        verbose_name_plural = "강의제목"

# 상세 강의 리스트
class lectureList(models.Model):
    lecture_list = models.ForeignKey(lectureTitle, on_delete=models.CASCADE, verbose_name='강의리스트')
    title        = models.CharField(max_length=50, verbose_name='제목')
    contents     = models.TextField(max_length=200, verbose_name='설명')
    image        = models.ImageField(upload_to='lecture/list/detail/img/',blank=True, null=True, verbose_name='이미지')

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

        super(lectureList,self).delete(*args, **kargs)

    class Meta:
        db_table = "lecture_list"
        verbose_name = "강의리스트"
        verbose_name_plural = "강의리스트"