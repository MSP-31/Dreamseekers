import os ,shutil
from django.db import models

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# 게시글
class Post(models.Model):
    author     = models.ForeignKey('user.Users', on_delete=models.CASCADE,related_name='board_posts', verbose_name='글쓴이')
    title      = models.CharField(max_length=50, verbose_name='제목')
    contents   = models.TextField(max_length=3000, verbose_name='내용')
    photo      = models.ImageField(upload_to='img', blank=True, null=True, verbose_name='이미지')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='수정일')
    is_private = models.BooleanField(default=False, verbose_name='비밀글')
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # 모델을 먼저 저장하여 pk값 취득
        super().save(*args, **kwargs)
        
        # 이미지가 존재하는 경우
        if self.photo:
            old_file_path = self.photo.path
            new_file_path = f'board/{self.pk}/{self.photo.name}'

            if not default_storage.exists(new_file_path):
                # 파일을 새 위치로 복사
                file_content = ContentFile(self.photo.read())
                new_file = default_storage.save(new_file_path,file_content)
                
                # 파일 핸들 닫기
                file_content.close()
                self.photo.close()

                # 원본 삭제
                default_storage.delete(old_file_path)
                # 파일 필드 업데이트
                self.photo.name = new_file
            # 모델을 다시 저장하여 이미지 필드를 업데이트
            super(Post,self).save(update_fields=['photo'])
    
    # 게시글이 삭제되면 이미지도 같이 삭제
    def delete(self, *args, **kargs):
        if self.photo:
            try:
                # 이미지 삭제
                os.remove(self.photo.path)
                # 상위폴더 주소와서 삭제
                parent_dir = os.path.dirname(os.path.dirname(self.photo.path))
                shutil.rmtree(parent_dir)
            except FileNotFoundError:
                pass
        else: #이미지 파일이 없는 경우
            pass
        super(Post,self).delete(*args, **kargs)
    
    class Meta:
        db_table = "community_board"
        verbose_name = "게시물"
        verbose_name_plural = "게시물"