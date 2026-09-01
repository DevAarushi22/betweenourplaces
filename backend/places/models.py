from django.contrib.auth.models import User
from django.db import models

from relationships.models import Relationship


class Place(models.Model):
    relationship = models.ForeignKey(
        Relationship,
        on_delete=models.CASCADE,
        related_name="places",
    )

    name = models.CharField(max_length=200)

    address = models.TextField(blank=True)

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
    )

    google_place_id = models.CharField(
        max_length=255,
        blank=True,
    )

    category = models.CharField(
        max_length=50,
        blank=True,
    )

    note = models.TextField(blank=True)

    added_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="added_places",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.name