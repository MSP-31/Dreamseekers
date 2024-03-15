from django.contrib import admin
from lecture.models import Inquiry,lectureCalender,lectureTitle,lectureList

class InquiryAdmin(admin.ModelAdmin):
    list_display = ('title','author','phone','created_at',)

class lectureCalenderAdmin(admin.ModelAdmin):
    list_display = ('date','contents','allDay')

class lectureTitleAdmin(admin.ModelAdmin):
    list_display = ('title','image',)

class lectureListAdmin(admin.ModelAdmin):
    list_display = ('title','lecture_list',)

admin.site.register(Inquiry,InquiryAdmin)
admin.site.register(lectureCalender,lectureCalenderAdmin)
admin.site.register(lectureTitle,lectureTitleAdmin)
admin.site.register(lectureList,lectureListAdmin)
# Register your models here.
