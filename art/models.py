from datetime import date

from django.db import models
from users.models import Seller
# Create your models here.
class art_listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
    artist_name = models.CharField(max_length=255)
    style = models.CharField(max_length=255)
    medium = models.CharField(max_length=255)
    year_created = models.DateField(default=date.today, null=True, blank=True)
    edition = models.CharField(max_length=255, null=True, blank=True)
    provenance = models.TextField(max_length=500, null=True, blank=True)
    date_added = models.DateField(default=date.today)
    starting_price = models.IntegerField(default=0)
    current_bid = models.IntegerField(default=0)
    mimimum_bid = models.IntegerField(default=0)
    # weight_kg = models.FloatField(default=0)
    # thumbnail_image_url = models.ForeignKey("art_image", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} by {self.artist_name} \n{self.medium}"

class art_image(models.Model):
    id = models.AutoField(primary_key=True)
    listing_id = models.ForeignKey(art_listing, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_thumbnail = models.BooleanField(default=False)
    description = models.TextField(max_length=500)
