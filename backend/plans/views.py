from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from relationships.services import get_user_relationship
from .services import create_plan, finalize_plan, reveal_plan

from .models import Plan
from .serializers import (
    PlanCreateSerializer,
    PlanFinalizeSerializer,
    PlanListSerializer,
)
from .services import (
    create_plan,
    finalize_plan,
)


class PlanListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        relationship = get_user_relationship(request.user)

        if relationship is None:
            return Response(
                {
                    "detail": (
                        "You are not part of a relationship."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        plans = relationship.plans.order_by(
            "-date",
            "-created_at",
        )

        serializer = PlanListSerializer(
            plans,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = PlanCreateSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        relationship = get_user_relationship(request.user)

        if relationship is None:
            return Response(
                {
                    "detail": (
                        "You are not part of a relationship."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        plan = create_plan(
            relationship=relationship,
            user=request.user,
            validated_data=serializer.validated_data,
        )

        return Response(
            {
                "id": plan.id,
                "status": plan.status,
                "planning_type": plan.planning_type,
            },
            status=status.HTTP_201_CREATED,
        )


class PlanToPlanView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        relationship = get_user_relationship(request.user)

        if relationship is None:
            return Response(
                {"detail": "You are not part of a relationship."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        plans = relationship.plans.filter(
            planner=request.user,
            status=Plan.Status.WAITING_FOR_PLANNER,
        ).order_by("date", "created_at")

        serializer = PlanListSerializer(plans, many=True)

        return Response(serializer.data)


class PlanFinalizeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, plan_id):
        relationship = get_user_relationship(request.user)

        if relationship is None:
            return Response(
                {
                    "detail": (
                        "You are not part of a relationship."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        plan = relationship.plans.filter(
            id=plan_id
        ).first()

        if plan is None:
            return Response(
                {
                    "detail": "Plan not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PlanFinalizeSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        try:
            plan = finalize_plan(
                plan=plan,
                user=request.user,
                validated_data=serializer.validated_data,
            )
        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "id": plan.id,
                "status": plan.status,
                "planning_type": plan.planning_type,
                "location_revealed": plan.location_revealed,
            },
            status=status.HTTP_200_OK,
        )

class PlanRevealView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, plan_id):
        relationship = get_user_relationship(request.user)

        if relationship is None:
            return Response(
                {"detail": "You are not part of a relationship."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        plan = relationship.plans.filter(id=plan_id).first()

        if plan is None:
            return Response(
                {"detail": "Plan not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            plan = reveal_plan(
                plan=plan,
                user=request.user,
            )
        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "id": plan.id,
                "status": plan.status,
                "planning_type": plan.planning_type,
                "location_revealed": plan.location_revealed,
            },
            status=status.HTTP_200_OK,
        )