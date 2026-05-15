from http.client import HTTPResponse

from django.shortcuts import render, redirect, get_object_or_404

from art.forms.listing_create_form import ListingCreateForm
from users.models import Seller, Profile
from art.models import ListingImage
from django.contrib.auth.decorators import login_required
from django.utils import timezone


# Create your views here.

def index(request):
    return HTTPResponse(f"Response from {request.path}")

@login_required(login_url="/login/")
def create_listing(request):
    if not request.user.profile.is_seller:
        return redirect("create_seller")
    form = ListingCreateForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        listing = form.save(commit=False)

        profile, _ = Profile.objects.get_or_create(user=request.user)
        seller, _ = Seller.objects.get_or_create(profile=profile)

        listing.seller = seller
        listing.date_added = timezone.now()
        listing.current_bid = listing.starting_bid
        listing.save()

        images = request.FILES.getlist('images')
        images.insert(0, listing.thumbnail_image)

        for i, image in enumerate(images):
            ListingImage.objects.create(
                listing=listing,
                image=image,
                is_primary=(i == 0)
            )

        return redirect("artwork", id=listing.id)

    return render(request, "art/create_listing.html", {"form": form})
