from django.db import models

from django.contrib.auth.models import User
# Create your models here.



class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    user_address = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to="profiles/", default="profiles/default_profile.png", null=True, blank=True)
    is_seller = models.BooleanField(default=False)
    def __str__(self):
        return f" {self.user.username} {self.profile_image}"

class Seller(models.Model):
    TYPE_CHOICES = [
        ('Individual', 'individual'),
        ('Gallery', 'gallery'),
    ]
    id = models.AutoField(primary_key=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    street = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return f"{self.profile.user.username} {str(self.id)}"