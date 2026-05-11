from http.client import HTTPResponse

from django.shortcuts import render, redirect

from art.forms.listing_create_form import ListingCreateForm
from users.models import Seller, Profile
from art.models import art_listing, ListingImage
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return HTTPResponse(f"Response from {request.path}")

@login_required
def create_listing(request):
    form = ListingCreateForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            listing = form.save(commit=False)

            profile, _ = Profile.objects.get_or_create(user=request.user)
            seller, _ = Seller.objects.get_or_create(profile=profile)

            listing.seller = seller
            listing.save()

            images = request.FILES.getlist('images')
            for image in images:
                ListingImage.objects.create(
                    listing=listing,
                    image=img,
                    is_primary=(i == 0)
                )


            return redirect("artwork")

    return render(request, "art/create_listing.html", {"form": form})