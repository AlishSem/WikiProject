from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry, name="entry"), 
    path("search/", views.search, name="search"),
    path("newpage/", views.newpage, name = "newpage"),
    path("<str:title>/edit", views.edit, name = "edit"),
    path("randompage/", views.random, name = "random")
]



