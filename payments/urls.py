from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("here/", views.dues_list, name="dues_list"),
]