import uuid

from django.conf import settings
from django.db import models

from dues.models import Dues


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dues = models.ForeignKey(Dues, on_delete=models.RESTRICT, related_name="payments")
    payment_date = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    transaction_id = models.CharField(
        max_length=255, blank=True, null=True
    )  # Store unique transaction ID from the payment gateway

    def __str__(self):
        return f"{self.user.first_name} - {self.is_verified} on {self.payment_date.strftime('%Y-%m-%d %H:%M:%S')}"
