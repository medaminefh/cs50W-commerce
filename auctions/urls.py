from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("create", views.create, name="create"),
    path("listing/<int:id>/", views.listing, name="listing"),
    path("listing/<str:category>/",
         views.category_listing, name="category_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:id>", views.toggle_watchlist, name="toggle_watchlist"),
    path("categories", views.categories, name="categories"),
    path("close/<int:id>", views.close, name="close"),
    path("inactive", views.inactive, name="inactive"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
