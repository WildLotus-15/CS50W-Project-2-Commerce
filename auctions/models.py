from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    image_url = models.URLField(blank=True, max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}: {self.description} price=${self.price}"
    
    def get_absolute_url(self):
        return reverse('index',)
    
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, related_name="bids", null=True)
    starting_bid = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.auction}'s starting bid {self.starting_bid}"
    
class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, related_name="comments", null=True)
    comment = models.CharField(max_length=255)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.author}: {self.comment}"