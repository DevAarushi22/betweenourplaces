from django.urls import path

from .views import (
    PlanFinalizeView,
    PlanListCreateView,
    PlanRevealView,
    PlanToPlanView,
)

urlpatterns = [
    path("", PlanListCreateView.as_view(), name="plan-list-create"),
    path("to-plan/", PlanToPlanView.as_view(), name="plan-to-plan"),
    path(
        "<int:plan_id>/finalize/",
        PlanFinalizeView.as_view(),
        name="plan-finalize",
    ),
    path(
        "<int:plan_id>/reveal/",
        PlanRevealView.as_view(),
        name="plan-reveal",
    ),
]