from django.contrib import admin
from django.urls import path, include

from main.views import main

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main),
    path('/', include('main.urls')),
    path('user/',include('user.urls'))
]
