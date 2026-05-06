from django.db import models

# Create your models here.
class users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f" {self.username} {str(self.id)}"

class sellers(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(users, on_delete=models.CASCADE)
    is_gallery = models.BooleanField(default=False)
    address = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.user_id.username} {str(self.id)}"