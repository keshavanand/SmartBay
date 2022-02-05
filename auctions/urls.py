from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.createListing, name="createListing"),
    path("listing/<str:title>", views.listingDetail, name="listingDetail"),
    path("watchlist", views.watchlist,name="watchlist"),
    path("addtoWatchlist/<str:title>",views.addToWatchlist,name="addToWatchlist"),
    path("removeFromWatchlist/<str:title>",views.removeFromWatchlist,name="removeFromWatchlist"),
    path("closeListing/<str:title>",views.closeListing,name="closeListing"),
    path("addComment/<str:title>",views.addComment,name="addComment"),
    path("category/<str:name>",views.category,name="category")
]
