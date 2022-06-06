from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'reliable/index.html')

def pricing(request):
    return render(request, 'reliable/pricing.html')

