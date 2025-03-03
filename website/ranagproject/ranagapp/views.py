from django.shortcuts import render

def home(request):
    return render(request, 'sitefiles/index.html')

def download(request):
    return render(request, 'sitefiles/download.html')