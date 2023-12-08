from django.contrib import admin
from course.models import Course

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name','description','image',)

admin.site.register(Course, CourseAdmin)