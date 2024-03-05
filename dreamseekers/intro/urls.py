from django.urls import path
from .views import greeting, instructors, instrs_delete, contact

app_name = 'intro'

urlpatterns = [
    path('greeting/',greeting, name='greeting'),

    path('instructors/',instructors,name='instructors'),
    path('instructors/delete/<int:pk>',instrs_delete,name="instrs_del"),

    path('contact/',contact, name="contact"),
]