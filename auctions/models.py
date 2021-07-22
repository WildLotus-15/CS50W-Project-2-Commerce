from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=30)
    
    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    current_bid = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name="similar_listings")
    creator = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name="creator") 
    image_url = models.URLField(blank=True, max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}: {self.description}"
    
    def get_absolute_url(self):
        return reverse('index')
    
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, related_name="bids", null=True)
    offer = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.auction}'s starting bid {self.offer}"
    
class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, related_name="comments", null=True)
    comment = models.CharField(max_length=255)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.comment}"