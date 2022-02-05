from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,Listing,Bid,Category,Comment, Watchlist
from django import forms


def index(request):
    listing=Listing.objects.all()
    categories=Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings":listing,
        "categories": categories
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
            watchlist=Watchlist.objects.create_Watchlist(user)
            watchlist.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

class CreateListingForm(forms.Form):
    title=forms.CharField(max_length=255)
    startingBid=forms.FloatField()
    description=forms.CharField(max_length=1000)




@login_required(login_url='login')
def createListing(request):
    if request.method=="POST":
        title=request.POST['title']
        startingbid=float(request.POST['startingBid'])
        description=request.POST['description']
        image=request.POST['image']
        category=Category.objects.get(name=request.POST['category'])
        user=request.user
        
        listing=Listing.objects.create_listing(title,startingbid,description,category,image,user)

        categoryList=Category.objects.all()

        return render(request, "auctions/createListing.html",{
            "message": 'Listing Created Successfully',
            "categoryList": categoryList
            
        })
    else:
        categoryList=Category.objects.all()
        return render(request, "auctions/createListing.html",{
            "categoryList": categoryList
        })


def listingDetail(request,title):
    listing=Listing.objects.get(title=title)
    category=listing.category.all()
    user=request.user
    
    comments=reversed(Comment.objects.filter(listing=listing))


    createdByLoggedInUser=None
    if listing.user==user:
        createdByLoggedInUser=True
    else:
        createdByLoggedInUser=False



    higgestBid=listing.bidding.all().aggregate(Max('bid'))['bid__max']
    totalBids=len(listing.bidding.all())
    bidder=None
    inWatchlist=None  # None is False in case of boolean
    if user.is_authenticated:
        watchlist=Watchlist.objects.get(user=user)
        items=watchlist.items.all()
        
        if listing in items:
           inWatchlist=True
        else:
           inWatchlist=False


    if higgestBid:
       bidder=Bid.objects.get(listing=listing,bid=higgestBid)
    else:
        higgestBid=0
        totalBids=0
    if request.method=="POST":
        if user.is_authenticated:
            bid=float(request.POST['bid'])
            if bid >= listing.startingBid and bid > higgestBid:
                newBid=Bid.objects.create_bid(user,listing,bid)
                bidder=Bid.objects.get(listing=listing,bid=bid)
                totalBids=len(listing.bidding.all())
                return render(request, "auctions/listingDetail.html",{
                     "title": title,
                     "listing": listing,
                     "category": category,
                     "bidder": bidder,
                     "higgestBid": bid,
                     "totalBids": totalBids,
                     "inWatchlist": inWatchlist,
                     "createdByLoggedInUser": createdByLoggedInUser,
                     "active": listing.active,
                     "comments": comments
                    })  
            else:
                 return render(request, "auctions/listingDetail.html",{
                     "title": title,
                     "listing": listing,
                     "category": category,
                     "bid": bid,
                     "bidder": bidder,
                     "message": "Bid must be greater than previous one",
                     "higgestBid": higgestBid,
                     "totalBids": totalBids,
                     "inWatchlist": inWatchlist,
                     "createdByLoggedInUser": createdByLoggedInUser,
                     "active": listing.active,
                     "comments": comments
                    })
        else:
            return HttpResponseRedirect(reverse("login"))

    else:

        return render(request, "auctions/listingDetail.html",{
             "title": title,
             "listing": listing,
             "category": category,
             "bidder": bidder,
             "higgestBid": higgestBid,
             "totalBids": totalBids,
             "inWatchlist": inWatchlist,
             "createdByLoggedInUser": createdByLoggedInUser,
             "active": listing.active,
             "comments": comments
    
            })

def closeListing(request,title):
    if request.method=="POST":
        listing=Listing.objects.get(title=title)
        listing.active=False
        listing.save()
        return HttpResponseRedirect(reverse("listingDetail", args=[title]))

@login_required(login_url="login")
def watchlist(request):
    watchlist=Watchlist.objects.get(user=request.user)
    items=watchlist.items.all()
    return render(request, "auctions/watchlist.html",{
        "items": items
    })


@login_required(login_url="login")
def addToWatchlist(request,title):
    if request.method=="POST":
        user=request.user
        listing=Listing.objects.get(title=title)
        watchlist=Watchlist.objects.get(user=user)
        watchlist.items.add(listing)
    return HttpResponseRedirect(reverse("listingDetail", args=[title]))
   



def removeFromWatchlist(request,title):
    if request.method=="POST":
        user=request.user
        listing=Listing.objects.get(title=title)
        watchlist=Watchlist.objects.get(user=user)
        watchlist.items.remove(listing)
        items=watchlist.items.all()
    return render(request,"auctions/watchlist.html",{
        "items": items,
        "message": f"{title} removed from watchlist"
    })

@login_required(login_url="login")
def addComment(request,title):
    if request.method=="POST":
        comment=request.POST['comment']
        listing=Listing.objects.get(title=title)
        user=request.user

        Comment.objects.create_comment(user=user,listing=listing,comment=comment)
        
        return HttpResponseRedirect(reverse("listingDetail", args=[title]))


def category(request,name):
    categories=Category.objects.all()
    listings=Category.objects.get(name=name).allListing.all()
    return render(request,"auctions/category.html",{
        "categories": categories,
        "listings": listings,
        "name": name
    })