from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('listing/<int:listing_id>', views.listing, name="listing"),
    path('listing/<int:pk>/delete', views.DeleteListing.as_view(), name="listing_delete"),
    path('listing/new', views.newListing, name="add")
]
