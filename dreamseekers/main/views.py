from django.shortcuts import render

def main(request):
    return render(request, 'main.html',{})

def lecture(request):
    return render(request, 'lecture.html')