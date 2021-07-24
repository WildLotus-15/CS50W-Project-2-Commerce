from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('<int:listing_id>', views.listing, name="listing"),
    path('<int:listing_id>', views.take_bid, name="take_bid"),
    path('<int:listing_id>', views.add_comment, name="add_comment"),
    path('listing/new', views.newListing, name="add")
]
