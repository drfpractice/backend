from django.shortcuts import render, redirect
from  authentication.models import Student
from django.http import HttpResponse

def sH(request):
    return HttpResponse("Hello, world!")
