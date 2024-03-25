from django.contrib import admin
from .models import Post

class BoardAdmin(admin.ModelAdmin):
    list_display = ('title','author','created_at','is_private',)

admin.site.register(Post,BoardAdmin)