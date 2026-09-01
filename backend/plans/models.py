from django.contrib.auth.models import User
from django.db import models

from places.models import Place
from relationships.models import Relationship


class Plan(models.Model):

    class PlanningType(models.TextChoices):
        TOGETHER = "TOGETHER", "We plan"
        SURPRISE = "SURPRISE", "You surprise me"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        WAITING_FOR_PLANNER = (
            "WAITING_FOR_PLANNER",
            "Waiting for planner",
        )
        PLANNED = "PLANNED", "Planned"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    relationship = models.ForeignKey(
        Relationship,
        on_delete=models.CASCADE,
        related_name="plans",
    )

    requested_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="requested_plans",
    )

    planner = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name="planned_dates",
    null=True,
    blank=True,
    )

    mood = models.JSONField(
        default=list,
    )

    energy = models.PositiveSmallIntegerField()

    date = models.DateField()

    time_vibe = models.CharField(
        max_length=30,
    )

    planning_type = models.CharField(
        max_length=20,
        choices=PlanningType.choices,
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    place = models.ForeignKey(
    Place,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="plans",
    )

    location_revealed = models.BooleanField(
        default=True,
    )

    start_time = models.TimeField(
        null=True,
        blank=True,
    )

    end_time = models.TimeField(
        null=True,
        blank=True,
    )

    note = models.TextField(
        blank=True,
    )

    google_event_id = models.CharField(
        max_length=255,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.date} - {self.planning_type}"