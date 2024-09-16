from django.shortcuts import render

from .models import Payment


def dues_list(request):
    return render(request, "payments/list.html")
