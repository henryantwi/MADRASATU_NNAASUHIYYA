from django.shortcuts import render

from .models import Dues

from payments.models import Payment

from payments.models import Payment

def index(request):
    return render(request, "payments/index.html")

def dues_list(request):
    dues = Dues.objects.all()
    user_payments = Payment.objects.filter(user=request.user, is_verified=True)
    paid_dues_ids = user_payments.values_list("dues_id", flat=True)

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

    context = {"dues_status": dues_status}
    return render(request, "payments/list.html", context)