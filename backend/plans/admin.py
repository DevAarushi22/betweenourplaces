from django.contrib import admin

from .models import Plan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "planning_type",
        "status",
        "requested_by",
        "place",
    )

    list_filter = (
        "planning_type",
        "status",
    )

    search_fields = (
        "note",
    )