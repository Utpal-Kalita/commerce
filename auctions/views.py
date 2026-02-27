from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import ListingForm
from .models import User, Listing, Bid
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    active_listings = Listing.objects.filter(isActive=True)
    
    return render(request, "auctions/index.html", {
        "listings": active_listings,
    })


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

@login_required
def create_listing(request):
    if request.method == "POST":
      form = ListingForm(request.POST)

      if form.is_valid():
        listing = form.save(commit=False)
        listing.owner = request.user

        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForm()
        return render (request, "auctions/create.html",{
            "form":form
        })

def listing_view(request, id):
    listing_obj = get_object_or_404(Listing, pk=id)
    comments = listing_obj.listing_comments.all()

    highest_bid = listing_obj.listing_bids.order_by('-amount').first()

    if highest_bid:
        current_price = highest_bid.amount
    else:
        current_price = listing_obj.starting_bid

    is_watching = False
    if request.user.is_authenticated:
        if listing_obj.watchlist.filter(id=request.user.id).exists():
            is_watching = True

    return render(request, "auctions/listing.html",{
        "listing": listing_obj,
        "comments": comments,
        "current_price": current_price,
        "highest_bid": highest_bid,
        "starting_bid": listing_obj.starting_bid,
        "is_watching": is_watching


    })

@login_required
def place_bid(request, id):

    if request.method != "POST":
        return redirect("listing", id=id)


    listing_obj = get_object_or_404(Listing, pk=id)
    highest_bid = listing_obj.listing_bids.order_by('-amount').first()

    current_price = highest_bid.amount if highest_bid else listing_obj.starting_bid

    try:
        bid_amount = float(request.POST['bid'])
    except (TypeError, ValueError):
        messages.error(request, "Invalid bid amount.")
        return redirect("listing", id=id)

    if bid_amount > current_price:
        Bid.objects.create (
            user= request.user,
            listing = listing_obj,
            amount = bid_amount
        )

        messages.success(request, "Bid placed successfully!")

    else:
        messages.error(request, "Bid must be higher than current price.")

    return redirect("listing", id=id)


def toggle_watchlist(request, id):
    # Kick out users who aren't logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    listing_obj = get_object_or_404(Listing, pk=id)

    if listing_obj.watchlist.filter(id=request.user.id).exists():
        listing_obj.watchlist.remove(request.user)
    else:
        listing_obj.watchlist.add(request.user)
    return redirect ("listing", id=id)


@login_required
def close_auction(request, id):

    if request.method != "POST":
        return redirect("listing", id=id)

    listing_obj = get_object_or_404(Listing, pk=id)

    # Already closed
    if not listing_obj.isActive:
        messages.error(request, "Auction is already closed.")
        return redirect("listing", id=id)

    # Only owner can close
    if listing_obj.owner != request.user:
        messages.error(request, "You are not allowed to close this auction.")
        return redirect("listing", id=id)

    highest_bid = listing_obj.listing_bids.order_by('-amount').first()

    listing_obj.isActive = False

    if highest_bid:
        listing_obj.winner = highest_bid.user
        messages.success(request, "Auction closed. Winner selected.")
    else:
        messages.info(request, "Auction closed. No bids were placed.")

    listing_obj.save()

    return redirect("listing", id=id)


@login_required
def watchlist_view(request):
    listings = request.user.watchlist_listings.all()
    return render(request, "watchlist.html",{
        "listings": listings,

    })



