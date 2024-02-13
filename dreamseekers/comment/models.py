from django.db import models

from board.models import Post
from lecture_inquiry.models import Inquiry

# 댓글
class Comment(models.Model):
    user = models.ForeignKey('user.Users',on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    parent = models.ForeignKey('self',related_name='reply',on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__ (self):
        return self.content
    
    class Meta:
        db_table = "community_comment"
        verbose_name = "댓글"
        verbose_name_plural = "댓글"

# 중간 DB
class PostCommetns(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    post    = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE, null=True, blank=True)