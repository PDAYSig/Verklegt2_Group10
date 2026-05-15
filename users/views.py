from multiprocessing import context

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from art.models import art_listing, Bid, Sale
from users.forms.create_seller_form import CreateSellerForm
from users.forms.create_user_form import CreateProfileForm
from art.forms.complete_payment_form import CompletePaymentForm
from art.forms.payment_type_forms import CreditCardForm, BankTransferForm, WireTransferForm
from users.models import Profile, Seller
from decimal import Decimal
from django.utils import timezone
from django.db.models import Min, Max
# Create your views here.

"""
this show our landing page with new listing which should only show the newest art and has not expired
there also is the recently sold which shows 2 recently sold artwork
and there is also the function which shows active bids
"""
def index(request):
    #shows active bids
    active_bid_items = art_listing.objects.filter(
        bids__expired_at__gt=timezone.now()
    ).distinct()

    #shows the 2 most recently sold artwork
    recently_sold_items = art_listing.objects.filter(
        bids__expired_at__lte=timezone.now()
    ).distinct().order_by('-bids__expired_at')[:2]

    # collects all artwork with expired bids
    expired_listing_ids = art_listing.objects.filter(
        bids__expired_at__lte=timezone.now()
    ).values_list('id', flat=True)

    #makes sure to show the new listing which don't have expired bids
    all_items = art_listing.objects.exclude(
        id__in=expired_listing_ids
    ).order_by('-date_added').distinct()[:6]

    return render(request, "users/index.html", {
        "items": all_items,
        "active_bid_items": active_bid_items,
        "recently_sold_items": recently_sold_items,
    })

def about(request):
    return render(request, "users/about.html")

def artwork_list(request):
    price_range = art_listing.objects.aggregate(
        min_price=Min('price'),
        max_price=Max('price'),
    )

    context = {
        "min_price": price_range['min_price'] or 0,
        "max_price": price_range['max_price'] or 0,
    }
    return render(request, 'users/all_art.html', context)
def all_art(request):
    listings = art_listing.objects.all()
    search_filter = request.GET.get('search_filter')
    medium = request.GET.get('medium')
    sort = request.GET.get('sort')
    style = request.GET.get('style')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

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
    elif sort == "least_expensive":
        listings = listings.order_by('current_bid')
    elif sort == "most_expensive":
        listings = listings.order_by('-current_bid')

    if style == "Modern":
        listings = listings.filter(style='Modern')
    elif style == "Abstract":
        listings = listings.filter(style='Abstract')
    elif style == "Realism":
        listings = listings.filter(style='Realism')
    elif style == "Impressionism":
        listings = listings.filter(style='Impressionism')

    if min_price:
        try:
            listings = listings.filter(current_bid__gte=int(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            listings = listings.filter(current_bid__lte=int(max_price))
        except ValueError:
            pass


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
    highest_bid = item.bids.order_by('-amount').first()
    auction_active = latest_bid is None or latest_bid.expired_at > timezone.now()
    user_has_bid = False
    user_is_winner = False
    sale_exists = Sale.objects.filter(listing=item).exists()

    if request.user.is_authenticated:
        profile = request.user.profile
        seller, _ = Seller.objects.get_or_create(profile=profile)
        user_has_bid = Bid.objects.filter(listing=item, bidder=seller).exists()

        if highest_bid and highest_bid.bidder == seller:
            user_is_winner = True

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        if not auction_active:
            messages.error(request, 'This auction has ended.')
            return redirect('artwork', id=id)

        if item.seller == seller:
            messages.error(request, 'You cannot bid on this item.')
            return redirect('artwork', id=id)

        bid_amount = Decimal(request.POST.get('bid_amount'))

        if bid_amount > item.current_bid and bid_amount >= item.minimum_bid and bid_amount >= item.starting_price:
            bid = Bid.objects.create(listing=item, bidder=seller, amount=bid_amount)
            item.current_bid = bid_amount
            item.save()
            messages.success(request, f'Your bid of ${bid_amount} was placed successfully!')
        else:
            messages.error(request, 'Bid must be higher than current bid and at least the starting price.')

        return redirect('artwork', id=id)

    return render(request, 'users/artwork.html', {
        'item': item,
        'images': images,
        'latest_bid': latest_bid,
        'highest_bid': highest_bid,
        'auction_active': auction_active,
        'user_has_bid': user_has_bid,
        'user_is_winner': user_is_winner,
        'recently_sold_items': art_listing.objects.none(),
        'sale_exists': sale_exists,
    })
def recently_sold(request):
    recently_sold_items = art_listing.objects.filter(
        bids__expired_at__lte=timezone.now()
    ).distinct()
    return render(request, "users/recently_sold.html", {
        "items": recently_sold_items,
    })

def register(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        profile_form = CreateProfileForm(request.POST, request.FILES)
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
            seller = form.save(commit=False)
            profile = request.user.profile
            seller.profile = profile
            profile.is_seller = True
            profile.save()
            seller.save()
            return redirect("create_listing")
    else:

        form = CreateSellerForm()
    return render(request, 'users/create_seller.html', {"form": form})


@login_required
def update_bid_status(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)

    if bid.listing.seller.profile.user != request.user:
        return redirect('artwork', id=bid.listing.id)

    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Bid.STATUS_CHOICES):
            bid.status = status
            bid.save()
            return redirect('artwork', id=bid.listing.id)

    return render(request, 'users/update_bid_status.html', {'bid': bid})

@login_required
def payment_info(request, bid_id):
    '''
    :param request:
    :param bid_id:
    User enters billing address, national id (SSN/'kennitala') and selects preferred payment method
    and gets redirected to the payment_details page
    '''
    bid = get_object_or_404(Bid, id=bid_id)
    if request.method == "POST":
        form = CompletePaymentForm(request.POST)
        if form.is_valid():
            # Save the session
            cleaned_data = form.cleaned_data
            request.session['payment_info'] = cleaned_data
            request.session['payment_method'] = cleaned_data['payment_method']
            return redirect('payment_details', bid_id = bid_id)
    else:
        form = CompletePaymentForm()
    return render(request, 'payments/payment_info.html', {
        'bid': bid,
        'form' : form
    })
def payment_details(request, bid_id):
    '''
    :param request:
    :param bid_id:
    Renders the payment details page where the user enters the card/bank details for the payment step
    and gets redirected to the payment_review page
    '''

    # Declaring the appropriate forms
    PAYMENT_FORMS = {
        "card" : CreditCardForm,
        "bank_transfer": BankTransferForm,
        "wire_transfer": WireTransferForm,
    }

    payment_method = request.session['payment_method']
    if request.method == "POST":
        # fetch the correct value and initialize it as a form object
        payment_form = PAYMENT_FORMS[payment_method]
        form = payment_form(request.POST)

        if form.is_valid():
            if payment_method == 'card':
                expiration_date = form.cleaned_data['expiration_date']
                request.session['payment_details'] = {
                    'card_number' : form.cleaned_data['card_number'][-4:],
                    'expiration_date' : str(expiration_date),
                }
            else:
                request.session['payment_details'] = form.cleaned_data

            return redirect('payment_review', bid_id=bid_id)
        # If the form has the wrong format, present the form again
        return redirect('payment_details', bid_id=bid_id)

    else:
        form = PAYMENT_FORMS[payment_method]
        return render(request, 'payments/payment_details.html', {'form' : form()})

def payment_review(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)
    info = request.session['payment_info']
    details = request.session['payment_details']
    if request.method == "POST":
        # Create the new object
        sale = Sale.objects.create(
            listing = bid.listing,
            buyer = request.user,
            seller = bid.listing.seller,
            payment_method=info["payment_method"],
            buyer_country=info["buyer_country"],
            buyer_city=info["buyer_city"],
            buyer_street=info["buyer_street"],
            buyer_postal_code=info["buyer_postal_code"],
            buyer_nid=info["buyer_nid"],
        )
        # Save the object
        sale.save()

        # Delete the session data
        del request.session['payment_details']
        del request.session['payment_info']
        del request.session['payment_method']

        return redirect('artwork', id=bid.listing.id)
    else:
        return render(request, 'payments/payment_review.html', {
        'info': info,
        'details': details
    })


@login_required
def edit_seller_profile(request):
    profile = request.user.profile
    seller = get_object_or_404(Seller, profile=profile)

    if request.method == "POST":
        seller.type = request.POST.get("seller_type", seller.type)
        seller.street = request.POST.get("street", seller.street)
        seller.city = request.POST.get("city", seller.city)
        seller.postal_code = request.POST.get("postal_code", seller.postal_code)
        if request.FILES.get("logo"):
            seller.logo = request.FILES.get("logo")
        if request.FILES.get("cover_image"):
            seller.cover_image = request.FILES.get("cover_image")
        seller.save()
        return redirect('profile')

    return render(request, "users/edit_seller_profile.html", {'seller': seller})


@login_required
def delete_listing(request, id):
    item = get_object_or_404(art_listing, id=id)

    if item.seller.profile.user != request.user:
        return redirect('artwork', id=id)

    if request.method == 'POST':
        item.delete()
        messages.success(request, ' deleted successfully.')
        return redirect('users-index')

    return render(request, 'users/delete_listing.html', {'item': item})