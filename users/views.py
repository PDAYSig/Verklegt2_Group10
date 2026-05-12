from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from art.models import art_listing, Bid
from users.forms.create_seller_form import CreateSellerForm
from users.forms.create_user_form import CreateProfileForm
from users.models import Profile, Seller
from decimal import Decimal
from django.utils import timezone
# Create your views here.

def index(request):
    all_items = art_listing.objects.all().order_by('-date_added')[:3]
    active_bid_items = art_listing.objects.filter(
        bids__expired_at__gt=timezone.now()
    ).distinct()

    return render(request, "users/index.html", {
        "items": all_items,
        "active_bid_items": active_bid_items,
    })

def all_art(request):
    listings = art_listing.objects.all()

    search_filter = request.GET.get('search_filter')
    medium = request.GET.get('medium')
    sort = request.GET.get('sort')
    style = request.GET.get('style')

    # if user types a name into the searchbar
    if search_filter:
        listings = listings.filter(title__icontains=search_filter)
    # if user selects a medium
    if medium:
        listings = listings.filter(medium=medium)
    # if user selects to sort by newest first
    if sort == "newest":
        listings = listings.order_by('-date_added')
    # if user selects to sort by oldest first
    elif sort == "oldest":
        listings = listings.order_by('date_added')

    if style == "Modern":
        listings = listings.filter(style='Modern')
    elif style == "Abstract":
        listings = listings.filter(style='Abstract')
    elif style == "Realism":
        listings = listings.filter(style='Realism')
    elif style == "Impressionism":
        listings = listings.filter(style='Impressionism')


    #TODO add extra filters for size and style
    return render(request, "users/all_art.html", {"listings": listings})

def login(request):
    return render(request, "users/login.html")

@login_required(login_url="/login/")
def profile(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    seller = Seller.objects.filter(profile=user_profile).first()

    if seller:
        from django.db.models import Max
        top_bids = (
            Bid.objects.filter(bidder=seller)
            .values('listing')
            .annotate(max_amount=Max('amount'))
        )
        bid_ids = []
        for b in top_bids:
            top_bid = Bid.objects.filter(
                bidder=seller,
                listing_id=b['listing'],
                amount=b['max_amount']
            ).first()
            if top_bid:
                bid_ids.append(top_bid.id)
        bids = Bid.objects.filter(id__in=bid_ids).order_by('-placed_at')
    else:
        bids = []

    if request.method == "POST":
        form = CreateProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect("profile")
    else:
        form = CreateProfileForm(instance=user_profile)

    return render(request, "users/profile.html", {
        "form": form,
        "user_profile": user_profile,
        "bids": bids,
    })

@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        bio = request.POST.get("bio")
        image = request.FILES.get("image")

        if bio is not None:
            profile.bio = bio

        if image:
            profile.profile_image = image

        profile.save()
        return redirect("profile")

    return render(request, "users/edit_profile.html")



def seller_profile(request, id):
    seller = get_object_or_404(Seller, profile__user__id=id)

    art = art_listing.objects.filter(seller=seller)

    return render(request, 'users/seller_profile.html', {
        'seller': seller,
        'art': art,
    })


def artwork(request, id):
    item = art_listing.objects.get(id=id)
    images = item.images.all()
    latest_bid = item.bids.last()
    auction_active = latest_bid is not None and latest_bid.expired_at > timezone.now()
    user_has_bid = False

    if request.user.is_authenticated:
        profile = request.user.profile
        seller, _ = Seller.objects.get_or_create(profile=profile)
        user_has_bid = Bid.objects.filter(listing=item, bidder=seller).exists()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        bid_amount = Decimal(request.POST.get('bid_amount'))
        if bid_amount > item.current_bid and bid_amount >= item.minimum_bid and bid_amount >= item.starting_price:
            Bid.objects.create(listing=item, bidder=seller, amount=bid_amount)
            item.current_bid = bid_amount
            item.save()
            latest_bid = item.bids.last()
            auction_active = True
            user_has_bid = True

    return render(request, 'users/artwork.html', {
        'item': item,
        'images': images,
        'latest_bid': latest_bid,
        'auction_active': auction_active,
        'user_has_bid': user_has_bid,
        'recently_sold_items': art_listing.objects.none()
    })
def recently_sold(request):
    return render(request, "users/recently_sold.html")
def user_by_id(request, id):
    return HttpResponse(f"response from {request.path} with id {id}")

def register(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        profile_form = CreateProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            users_profile = profile_form.save(commit=False)
            users_profile.user = user
            users_profile.save()
            return redirect("login")
        else:
            return render(request, "users/register.html", {
                "user_form": user_form,
                "profile_form": profile_form,
                "message": "form is invalid"})
    else:
        user_form = UserCreationForm(request.POST)
        profile_form = CreateProfileForm(request.POST)
    return render(request, "users/register.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })
@login_required
def create_seller(request):
    if request.method == "POST":
        form = CreateSellerForm(request.POST)
        if form.is_valid():
            print('its cool')
            seller = form.save(commit=False)
            profile = request.user.profile
            seller.profile = profile
            profile.is_seller = True
            profile.save()
            seller.save()
            return redirect("create_listing")
    else:
        print('Dumbass')
        form = CreateSellerForm()
    return render(request, 'users/create_seller.html', {"form": form})
