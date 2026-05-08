from django.shortcuts import render, redirect
from django.urls import path
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .models import users
# Create your views here.

def index(request):
    return render(request, "users/index.html")

def all_art(request):
    images = [f"https://picsum.photos/300?{i}" for i in range(1, 17)]
    return render(request, "users/all_art.html", {"images": images})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print("DEBUG:", username, password)  # check terminal

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("users-index")
        else:
            return render(request, "users/login.html", {
                "message": "Invalid username and/or password."
            })

    return render(request, "users/login.html")

def profile(request):
    user_obj = users.objects.first()

    return render(request, "users/profile.html", {
        "user_obj": user_obj
    })

def edit_profile(request):
    user_obj = users.objects.first()

    if user_obj is None:
        return HttpResponse("No users exist in database yet.")

    if request.method == "POST":
        user_obj.username = request.POST.get("username", user_obj.username)

        image = request.FILES.get("image")
        if image:
            user_obj.user_profile_image = image

        user_obj.save()
        return redirect("profile")

    return render(request, "users/edit_profile.html", {
        "user_obj": user_obj
    })

def seller_profile(request):
    return render(request, "users/seller_profile.html")

def artwork(request):
    return render(request, "users/artwork.html")

def recently_sold(request):
    return render(request, "users/recently_sold.html")
def user_by_id(request, id):
    return HttpResponse(f"response from {request.path} with id {id}")

