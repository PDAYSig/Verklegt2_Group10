from django.db import models

from django.contrib.auth.models import User
# Create your models here.



class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    password = models.CharField(max_length=255)
    user_address = models.CharField(max_length=255)
    profile_image = models.TextField(max_length=9999)
    def __str__(self):
        return f" {self.user_id.username} {self.profile_image}"

class Seller(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_gallery = models.BooleanField(default=False)
    rating = models.FloatField(default=0)
    def __str__(self):
        return f"{self.user_id.username} {str(self.id)}"