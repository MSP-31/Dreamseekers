from django.contrib import admin
from .models import Post

class BoardAdmin(admin.ModelAdmin):
    list_display = ('title','author',)

admin.site.register(Post,BoardAdmin)

# 참고 : https://iamthejiheee.tistory.com/59