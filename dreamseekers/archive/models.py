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
        db_table = "community_archive_imgs"

class File(models.Model):
    file = models.FileField(upload_to='file', blank=True, null=True)

    def delete(self, *args, **kwargs):
        # 파일이 실제로 존재하는 경우
        if os.path.isfile(self.file.path):
            try:
                # 삭제
                os.remove(self.file.path)
            except FileNotFoundError:
                pass
        # DB에서 기록 삭제
        super(File, self).delete(*args, **kwargs)

    class Meta:
        db_table = "community_archive_file"

# 자료실 게시글
class Archive(models.Model):
    author     = models.ForeignKey('user.Users', on_delete=models.CASCADE,related_name='board_Archive', verbose_name='글쓴이')
    title      = models.CharField(max_length=50, verbose_name='제목')
    contents   = models.TextField(max_length=3000, verbose_name='내용')
    image      = models.ManyToManyField(Image,blank=True, verbose_name='이미지')
    files      = models.ManyToManyField(File, blank=True, verbose_name='파일')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='수정일')
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
    # 모델을 먼저 저장하여 pk값 취득
        super().save(*args, **kwargs)
    
        # 추가할 이미지가 존재하는 경우
        for image in self.image.all():
            old_file_path = image.image.path
            new_file_path = f'archive/{self.pk}/{image.image.name}'

            # 이미지 파일 존재 여부 확인
            if 'archive' in old_file_path and str(self.pk) in old_file_path:
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
        
        # 추가할 파일이 존재하는 경우
        for file in self.files.all():
            old_file_path = file.file.path
            new_file_path = f'archive/{self.pk}/{file.file.name}'

            # 이미지 파일 존재 여부 확인
            if 'archive' in old_file_path and str(self.pk) in old_file_path:
                # 이미 존재하는 경우 처리 건너뛰기
                continue

            if not default_storage.exists(new_file_path):
                # 파일을 새 위치로 복사
                file_content = ContentFile(file.file.read())
                new_file = default_storage.save(new_file_path, file_content)
            
                # 파일 핸들 닫기
                file_content.close()
                file.file.close()

                # 원본 삭제
                default_storage.delete(old_file_path)
                # 파일 필드 업데이트
                file.file.name = new_file
                file.save()

        # 모델을 다시 저장하여 필드를 업데이트
        super(Archive, self).save()
   
    # 게시글이 삭제
    def delete(self, *args, **kargs):

        # 이미지가 존재하면 같이 삭제
        for image in self.image.all():
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

        # 파일이 존재하면 같이 삭제
        for file in self.files.all():
            if os.path.isfile(file.file.path):
                try:
                    # 이미지 삭제
                    os.remove(file.file.path)
                    # 상위폴더 주소와서 삭제
                    parent_dir = os.path.dirname(os.path.dirname(file.file.path))
                    shutil.rmtree(parent_dir)
                except FileNotFoundError:
                    pass
            else: #이미지 파일이 없는 경우
                pass
            file.delete()

        super(Archive,self).delete(*args, **kargs)
    
    class Meta:
        db_table = "community_archive"
        verbose_name = "자료실"
        verbose_name_plural = "자료실"
        