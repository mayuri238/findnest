from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    address = models.CharField(max_length=255)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='property_images/')
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
