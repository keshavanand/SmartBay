from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case
from django.db.models.fields import CharField




class User(AbstractUser):
    pass


class Category(models.Model):
    name=models.CharField(max_length=20)

    def __str__(self):
        return self.name

class ListingManager(models.Manager):
    def create_listing(self,t,s,d,c,i,u):
        listing=self.create(title=t,startingBid=s,description=d,image=i,user=u)
        listing.save()
        listing.category.add(c)
        listing.save()

        return listing

class Listing(models.Model):
    title=models.CharField(max_length=255)
    startingBid=models.FloatField(max_length=10)
    description=models.CharField(max_length=1000)
    category=models.ManyToManyField(Category, related_name="allListing")
    image=models.URLField(max_length=1000, blank=True)
    user=models.ForeignKey(User, on_delete=CASCADE, related_name="lister")
    active=models.BooleanField(default=True)

    objects=ListingManager()

    def __str__(self):
        return self.title


          
class BidManager(models.Manager):
    def create_bid(self,user,listing,bid):
        bid=self.create(user=user,listing=listing,bid=bid)
        bid.save()
        return bid


class Bid(models.Model):
    user=models.ForeignKey(User, on_delete=CASCADE, related_name="bidder")
    listing=models.ForeignKey(Listing, on_delete=CASCADE, related_name="bidding")
    bid=models.FloatField(max_length=10)

    objects=BidManager()

    def __str__(self):
        return str(self.bid)


class CommentManager(models.Manager):
    def create_comment(self,user,listing,comment):
        comment=self.create(user=user,listing=listing,comment=comment)
        comment.save()
        return comment



class Comment(models.Model):
    user=models.ForeignKey(User, on_delete=CASCADE, related_name="commenter")
    listing=models.ForeignKey(Listing, on_delete=CASCADE, related_name="comments")
    comment=models.CharField(max_length=1000)


    objects=CommentManager()

    def __str__(self):
        return self.comment

class WatchlistManager(models.Manager):
    def create_Watchlist(self,user):
        watchlist=self.create(user=user)
        watchlist.save()

        return watchlist

class Watchlist(models.Model):
    user=models.ForeignKey(User, on_delete=CASCADE, related_name="userWatchlist")
    items=models.ManyToManyField(Listing, blank=True, related_name="listingWatchlisting")

    objects=WatchlistManager()

    def __str__(self):
        return f"{str(self.user).capitalize()} watchlist"



