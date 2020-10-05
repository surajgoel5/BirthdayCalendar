from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse

from .tasks import *

def start(request):
    mailerFunc()
    return HttpResponse("Mailer Started")
