from django.shortcuts import render
from django.urls import path
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request, "users/index.html")
def user_by_id(request, id):
    return HttpResponse(f"response from {request.path} with id {id}")

