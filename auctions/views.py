from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from datetime import datetime

from .models import User,Listings,Bids,Comments,Categories, Watchlist


class BidForm(forms.Form):
    bid = forms.IntegerField(label="Bid Amount")

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":60}), label="")


def index(request):
    listings=Listings.objects.all()
    return render(request, "auctions/index.html", {
        "listings":listings
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


def create(request):
    categories = Categories.objects.all()
    return render(request,"auctions/create.html", {
        "categories":categories
    })


def submit(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        seller = request.user.username
        starting_bid = request.POST.get('starting_bid')
        category = request.POST.get('category')
        if request.POST.get('image_url'):
            image_url = request.POST.get('image_url')
        else:
            image_url = "NULL"

        newListing = Listings(title=title, description=description, seller=seller,
                                starting_bid=starting_bid, category=category, image_url=image_url)
        newListing.save()

    return HttpResponseRedirect(reverse("index"))


def categories(request):
    categories=Listings.objects.values('category').distinct()
    return render(request,"auctions/categories.html", {
        "categories":categories
    })


def category(request, category):
    listings=Listings.objects.filter(category=category)
    title=category
    return render(request,"auctions/index.html", {
        "listings":listings,
        "title":title
    })


def listing(request, id):
    listing=Listings.objects.get(id=id)
    try:
        comments = Comments.objects.filter(listing_id=id)
    except:
        comments = None
    try:
        if Watchlist.objects.get(watcher=request.user.username, listing_id=id):
            watching = True
    except:
        watching = False
    return render(request,"auctions/listingInfo.html", {
        "listing":listing,
        "watching":watching,
        "comments":comments,
        "form": BidForm(),
        "form2": CommentForm()
    })


def watchlist(request):
    username=request.user.username
    title="Watchlist Items"
    listings=Listings.objects.all()
    watchlist=Watchlist.objects.filter(watcher=username)

    if watchlist:
        empty=0
    elif username:
        empty=1
    else:
        empty=2
    return render(request,"auctions/index.html", {
        "listings":listings,
        "title":title,
        "watchlist":watchlist,
        "empty":empty
    })


def addToWatchlist(request, id):
    if request.user.username:
        newWatchlistItem = Watchlist(watcher=request.user.username, listing_id=id)
        newWatchlistItem.save()
    return redirect('listing',id=id)


def removeFromWatchlist(request, id):
    if request.user.username:
        try:
            oldWatchlistItem = Watchlist.objects.get(watcher=request.user.username, listing_id=id)
            oldWatchlistItem.delete()
        except:
            pass
    return redirect('listing',id=id)


def bid(request, id):
    listing=Listings.objects.get(id=id)
    currentBid=listing.starting_bid
    try:
        if Watchlist.objects.get(watcher=request.user.username, listing_id=id):
            watching = True
    except:
        watching = False
    if request.method == "POST":
        bid = int(request.POST.get('bid'))
        if bid > currentBid:
            listing.starting_bid = bid
            listing.save()
            newBid = Bids(bid=bid, listing_id=id, user=request.user.username)
            newBid.save()
            return redirect('listing',id=id)
        else:
            error=True
            return render(request,"auctions/listingInfo.html", {
                "listing":listing,
                "watching":watching,
                "form": BidForm(),
                "form2": CommentForm(),
                "error": error
            })

    if request.user.username:
        newWatchlistItem = Watchlist(watcher=request.user.username, listing_id=id)
        newWatchlistItem.save()
    return redirect('listing',id=id)

def closebid(request, id):
    listing=Listings.objects.get(id=id)
    listing.active = False
    listing.save()

    return redirect('listing',id=id)

def comment(request, id):
    comment = request.POST.get('comment')
    time=datetime.now().strftime("%m/%d/%Y %I:%M %p")
    if request.method == "POST":
        newComment = Comments(comment=comment, listing_id=id, user=request.user.username, posting_time=time)
        newComment.save()
        return redirect('listing',id=id)
