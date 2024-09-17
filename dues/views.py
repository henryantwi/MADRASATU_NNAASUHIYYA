from calendar import month_name
from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from payments.models import Payment

from .models import Dues


@login_required
def index(request):
    return render(request, "payments/index.html")


@login_required
def dues_list(request):
    payment_status = request.GET.get("payment_status")
    user_payments = Payment.objects.filter(user=request.user, is_verified=True)
    paid_dues_ids = user_payments.values_list("dues_id", flat=True)

    # Get the current date
    today = date.today()
    current_year = today.year
    current_month = today.month

    # Filter dues to show only months <= current month of the current year
    dues = Dues.objects.filter(
        month__year=current_year, month__month__lte=current_month
    )

    # Sort dues by month
    dues = sorted(
        dues,
        key=lambda due: list(month_name).index(due.month.strftime("%B")),
        reverse=True,
    )

    dues_status = []
    for due in dues:
        is_paid = due.id in paid_dues_ids
        dues_status.append(
            {
                "due": due,
                "is_paid": is_paid,
                "payment": user_payments.filter(dues=due).first() if is_paid else None,
            }
        )

    context = {
        "dues_status": dues_status,
        "payment_status": payment_status,
    }
    return render(request, "payments/list.html", context)
