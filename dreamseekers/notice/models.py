import os ,shutil
from django.db import models

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class Image(models.Model):
    image = models.ImageField(upload_to='img', blank=True, null=True)
    
    def delete(self, *args, **kwargs):
        # 이미지 파일이 실제로 존재하는 경우
        if os.path.isfile(self.image.path):
            try:
                # 이미지 삭제
                os.remove(self.image.path)
            except FileNotFoundError:
                pass
        # DB에서 이미지 기록 삭제
        super(Image, self).delete(*args, **kwargs)
    
    class Meta:
        db_table = "community_notice_imgs"

class File(models.Model):
    file = models.FileField(upload_to='img', blank=True, null=True)

# 게시글
class Notice(models.Model):
    author     = models.ForeignKey('user.Users', on_delete=models.CASCADE,related_name='board_Notices', verbose_name='글쓴이')
    title      = models.CharField(max_length=50, verbose_name='제목')
    contents   = models.TextField(max_length=3000, verbose_name='내용')
    photo      = models.ManyToManyField(Image,blank=True, verbose_name='이미지')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='수정일')
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
    # 모델을 먼저 저장하여 pk값 취득
        super().save(*args, **kwargs)
    
        # 이미지가 존재하는 경우
        for image in self.photo.all():
            old_file_path = image.image.path
            new_file_path = f'notice/{self.pk}/{image.image.name}'

            # 이미지 파일 존재 여부 확인
            if 'notice' in old_file_path and str(self.pk) in old_file_path:
                # 이미 존재하는 경우 처리 건너뛰기
                continue

            if not default_storage.exists(new_file_path):
                # 파일을 새 위치로 복사
                file_content = ContentFile(image.image.read())
                new_file = default_storage.save(new_file_path, file_content)
            
                # 파일 핸들 닫기
                file_content.close()
                image.image.close()

                # 원본 삭제
                default_storage.delete(old_file_path)
                # 파일 필드 업데이트
                image.image.name = new_file
                image.save()
        # 모델을 다시 저장하여 이미지 필드를 업데이트
        super(Notice, self).save()

    
    # 게시글이 삭제되면 이미지도 같이 삭제
    def delete(self, *args, **kargs):
        for image in self.photo.all():
            if os.path.isfile(image.image.path):
                try:
                    # 이미지 삭제
                    os.remove(image.image.path)
                    # 상위폴더 주소와서 삭제
                    parent_dir = os.path.dirname(os.path.dirname(image.image.path))
                    shutil.rmtree(parent_dir)
                except FileNotFoundError:
                    pass
            else: #이미지 파일이 없는 경우
                pass
            image.delete()
        super(Notice,self).delete(*args, **kargs)
    
    class Meta:
        db_table = "community_notice"
        verbose_name = "게시물"
        verbose_name_plural = "게시물"