from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=100 )
    def __str__(self):
        return self.category_name

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    img_url = models.URLField(blank=True, null=True) 
    isActive = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    @property
    def current_price(self):
        highest_bid = self.listing_bids.order_by('-amount').first()
        return highest_bid.amount if highest_bid else self.starting_bid
    
    @property
    def highest_bid_user(self):
        highest_bid = self.listing_bids.order_by('-amount').first()

        return highest_bid.user if highest_bid else None


#relationships
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "user_listings")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name= "category_listings", 
                                 blank=True, null=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name= "watchlist_listings")
    winner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
    related_name="won_auctions")
    def __str__(self):
        return self.title


class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
#relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "user_bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name= "listing_bids")
    def __str__(self):
        return f"{self.user} bid {self.amount} on {self.listing}"

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
#relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "user_comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name= "listing_comments")
    def __str__(self):
        return f"{self.user} commented {self.content} on {self.listing}"






