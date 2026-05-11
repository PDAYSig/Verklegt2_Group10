from datetime import date

from django.db import models
from users.models import Seller
# Create your models here.
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
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    artist_name = models.CharField(max_length=255)
    style = models.CharField(max_length=255, choices=STYLE_CHOICES)
    starting_price = models.IntegerField(default=0)
    medium = models.CharField(max_length=255, choices=MEDIUM_CHOICES)
    dimension = models.TextField(max_length=255)
    year_created = models.DateField(default=date.today, null=True, blank=True)
    edition = models.CharField(max_length=255, null=True, blank=True)
    provenance = models.TextField(max_length=500, null=True, blank=True)
    date_added = models.DateField(default=date.today)
    starting_price = models.IntegerField(default=0)
    current_bid = models.IntegerField(default=0)
    mimimum_bid = models.IntegerField(default=0)
    # weight_kg = models.FloatField(default=0)
    thumbnail_image = models.ImageField(
        upload_to='artworks/',
        null=True,
        blank=True
    )
    def __str__(self):
        return f"{self.title} by {self.artist_name} \n{self.medium}"

class ListingImage(models.Model):
    listing = models.ForeignKey(art_listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='artworks/')
    is_primary = models.BooleanField(default=False)
