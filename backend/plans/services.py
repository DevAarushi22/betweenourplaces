from places.models import Place

from .models import Plan


def create_plan(*, relationship, user, validated_data):
    planning_type = validated_data["planning_type"]

    other_member = (
        relationship.members
        .exclude(id=user.id)
        .first()
    )

    if other_member is None:
        raise ValueError(
            "Could not determine the other relationship member."
    )

    if planning_type == Plan.PlanningType.SURPRISE:
        status = Plan.Status.WAITING_FOR_PLANNER
        location_revealed = False
    else:
        status = Plan.Status.DRAFT
        location_revealed = True

    return Plan.objects.create(
        relationship=relationship,
        requested_by=user,
        planner=other_member,
        status=status,
        location_revealed=location_revealed,
        **validated_data,
    )


def finalize_plan(*, plan, user, validated_data):
    if plan.status != Plan.Status.WAITING_FOR_PLANNER:
        raise ValueError(
            "This plan is not waiting for a planner."
        )

    if plan.planning_type != Plan.PlanningType.SURPRISE:
        raise ValueError(
            "Only surprise plans can be finalized this way."
        )

    place = Place.objects.filter(
        id=validated_data["place_id"],
        relationship=plan.relationship,
    ).first()

    if place is None:
        raise ValueError(
            "This place does not belong to the relationship."
        )

    plan.place = place
    plan.start_time = validated_data["start_time"]
    plan.end_time = validated_data["end_time"]
    plan.note = validated_data.get("note", "")
    plan.status = Plan.Status.PLANNED
    plan.location_revealed = False

    plan.save()

    return plan