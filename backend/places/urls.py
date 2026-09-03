from django.urls import path

from .views import (
    PlaceDetailView,
    PlaceListCreateView,
)


urlpatterns = [
    path(
        "",
        PlaceListCreateView.as_view(),
        name="place-list-create",
    ),
    path(
        "<int:place_id>/",
        PlaceDetailView.as_view(),
        name="place-detail",
    ),
]