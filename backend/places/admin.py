from django.contrib import admin

from .models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "added_by",
        "created_at",
    )

    list_filter = (
        "category",
    )

    search_fields = (
        "name",
        "address",
    )