# dues/migrations/0002_populate_dues.py

from django.db import migrations, models
from django.utils import timezone
import random
import datetime

def populate_dues(apps, schema_editor):
    Dues = apps.get_model('dues', 'Dues')
    for month in range(1, 13):  # January (1) to December (12)
        # Generate a random amount between 50.00 and 200.00
        amount = round(random.uniform(50.00, 200.00), 2)
        # Create a date for each month in 2024
        month_date = datetime.date(2024, month, 1)
        # Create the Dues record
        Dues.objects.create(amount=amount, month=month_date)

class Migration(migrations.Migration):

    dependencies = [
        ('dues', '0001_initial'),  # Make sure this matches the previous migration
    ]

    operations = [
        migrations.RunPython(populate_dues),
    ]
    