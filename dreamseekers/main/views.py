from django.shortcuts import render

from .models import Slides

def main(request):
    slides = Slides.objects.all()

    return render(request, 'main.html',{'slides':slides})