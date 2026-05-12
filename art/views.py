from http.client import HTTPResponse

from django.shortcuts import render, redirect

from art.forms.listing_create_form import ListingCreateForm
from users.models import Seller, Profile
from art.models import ListingImage
from django.contrib.auth.decorators import login_required
from django.utils import timezone


# Create your views here.

def index(request):
    return HTTPResponse(f"Response from {request.path}")

@login_required
def create_listing(request):
    form = ListingCreateForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        listing = form.save(commit=False)

        profile, _ = Profile.objects.get_or_create(user=request.user)
        seller, _ = Seller.objects.get_or_create(profile=profile)

        listing.seller = seller
        listing.save()

        images = request.FILES.getlist('images')

        for i, image in enumerate(images):
            ListingImage.objects.create(
                listing=listing,
                image=image,
                is_primary=(i == 0)
            )

        return redirect("artwork", id=listing.id)

    return render(request, "art/create_listing.html", {"form": form})

def listing_detail(request, pk):
    item = get_object_or_404(ArtListing, pk=pk)

    if request.method == 'POST':
        bid_amount = Decimal(request.POST.get('bid_amount'))
        if bid_amount > item.current_bid and bid_amount >= item.minimum_bid:
            profile = request.user.profile
            Bid.objects.create(listing=item, bidder=profile, amount=bid_amount)
            item.current_bid = bid_amount
            item.save()

    return render(request, 'your_template.html', {'item': item})