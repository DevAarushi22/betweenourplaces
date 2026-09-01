from django.contrib.auth.models import User
from django.db import models


class Relationship(models.Model):
    name = models.CharField(max_length=100)

    members = models.ManyToManyField(
        User,
        related_name="relationships",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name
# Create your models here.
