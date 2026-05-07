from http.client import HTTPResponse

from django.shortcuts import render

from art.forms.listing_create_form import ListingCreateForm


# Create your views here.

def index(request):
    return HTTPResponse(f"Response from {request.path}")

def create_listing(request):
    if request.method == "POST":
        print(1)
    else:
        return render(request, 'art/create_listing.html', {
            'form' : ListingCreateForm()
        })