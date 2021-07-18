from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class User(AbstractUser):
    pass

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image_url = models.URLField(blank=True, max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}: {self.description}, price={self.price}"
    
class Bid(models.Model):
    auction = models.ManyToManyField(Auction, blank=True, related_name="bids")
    starting_bid = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.auction}'s starting bid {self.starting_bid}"
    
class Comment(models.Model):
    auction = models.ManyToManyField(Auction, blank=True, related_name="comments")
    comment = models.CharField(max_length=255)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.author}: {self.comment}"