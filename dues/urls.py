from django.urls import path

from . import views

app_name = "dues"

urlpatterns = [
    path("", views.index, name="index"),
    path("dues-list/", views.dues_list, name="dues_list"),

]
