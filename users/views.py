from django.shortcuts import render
from django.urls import path
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request, "users/index.html")

def all_art(request):
    images = [f"https://picsum.photos/300?{i}" for i in range(1, 17)]
    return render(request, "users/all_art.html", {"images": images})


def user_by_id(request, id):
    return HttpResponse(f"response from {request.path} with id {id}")

