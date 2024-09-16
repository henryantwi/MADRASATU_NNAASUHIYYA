import uuid

from django.db import models


class Dues(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Dues"
        verbose_name_plural = "Dues"

    def __str__(self):
        return f"{self.amount} for {self.month.strftime('%B')}, {self.month.year}"
