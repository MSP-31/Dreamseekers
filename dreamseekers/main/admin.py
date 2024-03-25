from django.contrib import admin
from .models import Slides

class SlidesAdmin(admin.ModelAdmin):
    list_display = ('title','contents')

admin.site.register(Slides,SlidesAdmin)
