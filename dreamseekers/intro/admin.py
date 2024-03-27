from django.contrib import admin
from .models import Intro,Instructors,Contact,BusinessInfo

class IntroAdmin(admin.ModelAdmin):
    list_display = ('title','contents')

class InstructorsAdmin(admin.ModelAdmin):
    list_display = ('name','contents')

class ContactAdmin(admin.ModelAdmin):
    list_display = ('address','sub_address','phone','sub_phone',)

class BusinessInfoAdmin(admin.ModelAdmin):
    list_display = ('rep','email','CRN','depositor',)

admin.site.register(Intro,IntroAdmin)
admin.site.register(Instructors,InstructorsAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(BusinessInfo,BusinessInfoAdmin)