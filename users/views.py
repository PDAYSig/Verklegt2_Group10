from django.shortcuts import render, redirect
from django.urls import path
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request, "users/index.html")

def all_art(request):
    images = [f"https://picsum.photos/300?{i}" for i in range(1, 17)]
    return render(request, "users/all_art.html", {"images": images})

def login(request):
    return render(request, "users/login.html")

def profile(request):
    return render(request, "users/profile.html")

def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        bio = request.POST.get("bio")
        image = request.FILES.get("image")

        if bio is not None:
            profile.bio = bio

        if image:
            profile.image = image

        profile.save()
        return redirect("profile")
    return render(request, "users/edit_profile.html")
def user_by_id(request, id):
    return HttpResponse(f"response from {request.path} with id {id}")

