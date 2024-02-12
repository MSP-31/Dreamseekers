from django.db import models

# 게시글
class Inquiry(models.Model):
    author     = models.ForeignKey('user.Users', on_delete=models.CASCADE, related_name='lecture_inquiry_posts', verbose_name='글쓴이')
    title      = models.CharField(max_length=50, verbose_name='제목')
    contents   = models.TextField(max_length=3000, verbose_name='내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "lecture_inquiry"
        verbose_name = "강의상담문의"
        verbose_name_plural = "강의상담문의"