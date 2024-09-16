from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("pay/<slug:uuid>/", views.make_payment, name="make_payment"),
    path("verify/<slug:ref>/", views.verify_payment, name="verify_payment"),
]
