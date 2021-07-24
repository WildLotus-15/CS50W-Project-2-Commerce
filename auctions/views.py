from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Listing, User, Comment, Bid
from django.views.generic import DeleteView
from django.forms import ModelForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class NewListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ('title', 'description', 'starting_bid', 'image_url', 'category')

class NewCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)

class NewBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['offer']

def newListing(request):
    if request.method == "POST":
        form = NewListingForm()
        if form.is_valid():
            NewListing = form.save()
            NewListing.creator = request.user
            NewListing.save()

    return render(request, "auctions/new.html", {
        'form': NewListingForm(),
        "success": True,
    })

def take_bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    offer = float(request.POST["offer"])
    if is_valid(offer, listing):
        listing.current_bid = offer
        form = NewBidForm(request.POST)
        newBid = form.save(commit=False)
        newBid.listing = listing
        newBid.author = request.user
        newBid.save()
        listing.save()
    else:
        render(request, "auctions/listing.html", {
        "bid_form": NewBidForm(),
        "listing": listing,
        "error_min_value": True
    })

def is_valid(offer, listing):
    if offer >= listing.starting_bid and listing.current_bid is None or offer > listing.current_bid:
        return True
    else:
        return False

def index(request):
    listings = Listing.objects.filter(active_listing=True)
    return render(request, "auctions/index.html", {
        "listing": listings
    })

def listing(request, listing_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    listing = Listing.objects.get(pk=listing_id)    
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": listing.comments.all(),
        "comment_form": NewCommentForm(),
        "bid_form": NewBidForm(),
    })

def add_comment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    form = NewCommentForm(request.POST)
    newComment = form.save(commit=False)
    newComment = Comment(listing=listing, author=request.user)
    newComment.save()

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
