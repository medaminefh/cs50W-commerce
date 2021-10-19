from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Watchlist, Bid, Comment


def index(request):
    listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
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


@login_required(login_url="/login")
def create(req):
    if req.method == "POST":
        title = req.POST['title']
        desc = req.POST['desc']
        img = req.POST['img']
        bid = req.POST['bid']
        categories = req.POST['cat']
        user = req.user
        if not img:
            newAuction = Listing.objects.create(
                title=title, description=desc, starting_bid=bid, category=categories, user=user)

        else:
            newAuction = Listing.objects.create(
                title=title, description=desc, img_url=img, starting_bid=bid, category=categories, user=user)
        newAuction.save()
        return HttpResponseRedirect(reverse("index"))
    return render(req, "auctions/create.html")


def inactive(req):
    listings = Listing.objects.filter(active=False)
    return render(req, 'auctions/index.html', {
        'listings': listings
    })


def listing(req, id):
    auction = Listing.objects.get(pk=id)
    if req.method == 'POST':
        user = req.user
        add_to_watchlist = Watchlist.objects.create(user=user, listing=auction)
        add_to_watchlist.save()
        return HttpResponseRedirect(reverse("index"))

    return render(req, 'auctions/auction.html', {
        "auction": auction
    })


def categories(req):
    return render(req, 'auctions/index.html')


def category_listing(req):
    return render(req, 'auctions/index.html')


@login_required(login_url="/login")
def watchlist(req):
    listings = Watchlist.objects.filter(user=req.user)
    print(listings)
    return render(req, 'auctions/watchlist.html', {
        'listings': listings
    })
