from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from relationships.services import get_user_relationship

from .models import Place
from .serializers import PlaceSerializer


class PlaceListCreateView(APIView):
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

        places = relationship.places.order_by("-created_at")

        serializer = PlaceSerializer(
            places,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):
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

        serializer = PlaceSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        place = Place.objects.create(
            relationship=relationship,
            added_by=request.user,
            **serializer.validated_data,
        )

        return Response(
            PlaceSerializer(place).data,
            status=status.HTTP_201_CREATED,
        )
class PlaceDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, place_id):
        relationship = get_user_relationship(request.user)

        if relationship is None:
            return Response(
                {"detail": "You are not part of a relationship."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        place = relationship.places.filter(id=place_id).first()

        if place is None:
            return Response(
                {"detail": "Place not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(PlaceSerializer(place).data)

    def patch(self, request, place_id):
        relationship = get_user_relationship(request.user)

        if relationship is None:
            return Response(
                {"detail": "You are not part of a relationship."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        place = relationship.places.filter(id=place_id).first()

        if place is None:
            return Response(
                {"detail": "Place not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PlaceSerializer(
            place,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, place_id):
        relationship = get_user_relationship(request.user)

        if relationship is None:
            return Response(
                {"detail": "You are not part of a relationship."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        place = relationship.places.filter(id=place_id).first()

        if place is None:
            return Response(
                {"detail": "Place not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        place.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)