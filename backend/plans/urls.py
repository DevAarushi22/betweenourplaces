from django.urls import path

from .views import (
    PlanFinalizeView,
    PlanListCreateView,
)


urlpatterns = [
    path(
        "",
        PlanListCreateView.as_view(),
        name="plan-list-create",
    ),

    path(
        "<int:plan_id>/finalize/",
        PlanFinalizeView.as_view(),
        name="plan-finalize",
    ),
]