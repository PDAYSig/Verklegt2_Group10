from django.db import models

# Create your models here.
class Art(models.Model):
    def __init__(self):
        self.id = models.AutoField(primary_key=True)
        self.title = models.CharField(max_length=200)
        self.description = models.TextField()
