from typing import NewType
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Watchlist, Bid, Comment


def index(request):
    listings = Listing.objects.filter(active=True)
    bids = Bid.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
        "bids": bids
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
    user = req.user
    bids = Bid.objects.filter(listing=auction)
    comments = Comment.objects.filter(listing=auction)

    highest_bid = auction.starting_bid

    if bids is not None:
        for bid in bids:
            if bid.value > highest_bid:
                highest_bid = bid.value

    exist_in_watch_list = ""

    try:

        exist_in_watch_list = Watchlist.objects.get(
            listing=auction, user=user)
    except:
        exist_in_watch_list = None

    if req.method == 'POST':

        bid = req.POST["bid"] or None
        comment = req.POST["comment"] or None

        try:
            bid = int(bid)
        except:
            bid = None

        def add_comment_or_bid(comment, bid):
            if comment is not None and bid is not None:
                new_comment = Comment.objects.create(
                    content=comment, user=user, listing=auction)
                new_comment.save()
                if bid < highest_bid:
                    return HttpResponseRedirect(reverse('listing', args=[id]))

                new_bid = Bid.objects.create(
                    value=int(bid), user=user, listing=auction)
                new_bid.save()

                delete_old_bids = Bid.objects.filter(
                    listing=auction).exclude(value=bid)
                delete_old_bids.delete()
                return HttpResponseRedirect(reverse("listing", args=[id]))
            else:
                if comment is not None:
                    new_comment = Comment.objects.create(
                        content=comment, user=user, listing=auction)
                    new_comment.save()
                    return HttpResponseRedirect(reverse('listing', args=[id]))

                if bid is not None:
                    if bid < highest_bid:
                        return HttpResponseRedirect(reverse('listing', args=[id]))

                    new_bid = Bid.objects.create(
                        value=int(bid), user=user, listing=auction)
                    new_bid.save()

                    delete_old_bids = Bid.objects.filter(
                        listing=auction).exclude(value=bid)
                    delete_old_bids.delete()

                    return HttpResponseRedirect(reverse('listing', args=[id]))
        return add_comment_or_bid(comment, bid)

    return render(req, 'auctions/auction.html', {
        "auction": auction, "user": user, "comments": comments, "highest_bid": highest_bid, "in_watchlist": exist_in_watch_list
    })


def categories(req):
    return render(req, 'auctions/index.html')


def category_listing(req):
    return render(req, 'auctions/index.html')


@login_required(login_url="/login")
def watchlist(req):
    listings = Watchlist.objects.filter(user=req.user)
    return render(req, 'auctions/watchlist.html', {
        'listings': listings
    })


@login_required(login_url="/")
def toggle_watchlist(req, id):
    user = req.user
    listing = Listing.objects.get(pk=id)

    watchlist = ""
    try:
        watchlist = Watchlist.objects.get(user=user, listing=listing)
    except:
        watchlist = None

    if watchlist is None:
        new_watchlist = Watchlist.objects.create(user=user,
                                                 listing=listing)
        new_watchlist.save()
        return HttpResponseRedirect(reverse("watchlist"))

    watchlist.delete()
    return HttpResponseRedirect(reverse("watchlist"))
