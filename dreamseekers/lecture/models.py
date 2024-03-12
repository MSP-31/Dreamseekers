from django.db import models
from django.core.validators import RegexValidator

# 게시글
class Inquiry(models.Model):
    author     = models.ForeignKey('user.Users', on_delete=models.CASCADE, related_name='lecture_posts', verbose_name='글쓴이')
    phoneNumberRegex = RegexValidator(regex = r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
    phone      = models.CharField(validators=[phoneNumberRegex], max_length=11, verbose_name='연락처')
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
    contents    = models.TextField(max_length=500, verbose_name='내용')
    date        = models.DateField(verbose_name='날짜')
    start_time  = models.TimeField(verbose_name='시작시간')
    end_time    = models.TimeField(verbose_name='종료시간')

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')
    
    # 게시글 삭제
    def delete(self, *args, **kargs):
        super(lectureCalender,self).delete(*args, **kargs)
    
    class Meta:
        db_table = "lecture_calender"
        verbose_name = "강의일정"
        verbose_name_plural = "강의일정"
