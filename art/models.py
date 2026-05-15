from datetime import date

from django.db import models
from django.contrib.auth.models import User
from users.models import Seller
from django.utils import timezone
from datetime import timedelta
# Create your models here.

"""
model class for art listing 
"""
class art_listing(models.Model):
    MEDIUM_CHOICES = [
        ('Oil', 'Oil'),
        ('Sculpture', 'Sculpture'),
        ('Acrylic', 'Acrylic'),
        ('Watercolour', 'Watercolour'),
        ('Photography', 'Photography'),
        ('Digital', 'Digital'),
    ]

    STYLE_CHOICES = [
        ('Modern', 'Modern'),
        ('Abstract', 'Abstract'),
        ('Realism', 'Realism'),
        ('Impressionism', 'Impressionism')
    ]
    id = models.AutoField(primary_key=True)

    #Artwork information
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    artist_name = models.CharField(max_length=255)
    year_created = models.DateField(default=date.today, null=True, blank=True)
    style = models.CharField(max_length=255, choices=STYLE_CHOICES)
    medium = models.CharField(max_length=255, choices=MEDIUM_CHOICES)
    dimension = models.TextField(max_length=255)
    edition = models.CharField(max_length=255, null=True, blank=True)
    provenance = models.TextField(max_length=500, null=True, blank=True)

    #Listing information
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    starting_price = models.IntegerField(default=0)
    date_added = models.DateField(default=date.today)
    current_bid = models.IntegerField(default=starting_price)
    minimum_bid = models.IntegerField(default=0)
    thumbnail_image = models.ImageField(upload_to='artworks/')

    def __str__(self):
        return f"{self.title} by {self.artist_name} \n{self.medium}"


"""
model class for listing images
"""
class ListingImage(models.Model):
    listing = models.ForeignKey(art_listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='artworks/')
    is_primary = models.BooleanField(default=False)


"""
model class for bids and bid functionality
"""
class Bid(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('contingent', 'Contingent'),
    ]

    listing = models.ForeignKey(art_listing, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(Seller, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    placed_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        if not self.pk:
            existing_bid = Bid.objects.filter(listing=self.listing).last()
            if existing_bid:
                self.expired_at = existing_bid.expired_at
            else:
                self.expired_at = timezone.now() + timedelta(days=1)
        super().save(*args, **kwargs)


"""
Model class for sales
"""
class Sale(models.Model):
    PAYMENT_CHOICES = [
        ('card', 'Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('wire_transfer', 'Wire Transfer'),]

    # Sale information
    id = models.AutoField(primary_key=True)
    listing = models.OneToOneField(art_listing, on_delete=models.CASCADE, related_name='sales')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    payment_method = models.CharField(max_length=255, choices=PAYMENT_CHOICES)

    # Buyer information
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer_nid = models.CharField(max_length=10)

    # Billing address
    buyer_country = models.CharField(max_length=255)
    buyer_city = models.CharField(max_length=255)
    buyer_street = models.CharField(max_length=255)
    buyer_postal_code = models.CharField(max_length=10)
