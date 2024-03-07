from django.contrib import admin
from lecture.models import Inquiry

class InquiryAdmin(admin.ModelAdmin):
    list_display = ('title','author','phone','created_at',)

admin.site.register(Inquiry,InquiryAdmin)
# Register your models here.
