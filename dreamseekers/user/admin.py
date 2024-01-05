from django.contrib import admin
from user.models import Users

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email',)

admin.site.register(Users, UserAdmin)
