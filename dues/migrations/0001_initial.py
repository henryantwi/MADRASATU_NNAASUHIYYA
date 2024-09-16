# Generated by Django 5.1.1 on 2024-09-16 01:47

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Dues",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("month", models.DateField()),
                ("date_created", models.DateTimeField(auto_now_add=True)),
            ],
            options={"verbose_name": "Dues", "verbose_name_plural": "Dues",},
        ),
    ]
