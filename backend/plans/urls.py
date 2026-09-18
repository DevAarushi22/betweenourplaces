from django.urls import path

from .views import (
    PlanFinalizeView,
    PlanListCreateView,
    PlanToPlanView,
)


urlpatterns = [
    path(
        "",
        PlanListCreateView.as_view(),
        name="plan-list-create",
    ),

    path(
        "to-plan/",
        PlanToPlanView.as_view(),
        name="plan-to-plan",
    ),

    path(
        "<int:plan_id>/finalize/",
        PlanFinalizeView.as_view(),
        name="plan-finalize",
    ),
]