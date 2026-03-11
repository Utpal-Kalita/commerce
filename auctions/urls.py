from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("listing/<int:id>", views.listing_view, name="listing"),
    path("listing/<int:id>/bid", views.place_bid, name="place_bid"),
    path("listing/<int:id>/watchlist", views.toggle_watchlist, name="toggle_watchlist"),
    path("listing/<int:id>/close", views.close_auction, name="close_auction"),
    path("listing/<int:id>/comment", views.add_comment, name="add_comment"),
    path("watchlist", views.watchlist_view, name="watchlist_view"),
    path("category", views.category_view, name="category_view"),
    path("category/<int:category_id>", views.category_listings, name="category_listing"),
    
    ]
