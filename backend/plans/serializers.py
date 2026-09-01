from rest_framework import serializers

from .models import Plan


class PlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            "mood",
            "energy",
            "date",
            "time_vibe",
            "planning_type",
        ]

    def validate_energy(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError(
                "Energy must be between 1 and 5."
            )

        return value

    def validate_mood(self, value):
        if not value:
            raise serializers.ValidationError(
                "Please choose at least one mood."
            )

        return value


class PlanListSerializer(serializers.ModelSerializer):
    place = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = [
            "id",
            "mood",
            "energy",
            "date",
            "time_vibe",
            "planning_type",
            "status",
            "place",
            "start_time",
            "end_time",
            "note",
            "location_revealed",
            "created_at",
        ]

    def get_place(self, obj):
        if not obj.place:
            return None

        if (
            obj.planning_type == Plan.PlanningType.SURPRISE
            and not obj.location_revealed
        ):
            return None

        return {
            "id": obj.place.id,
            "name": obj.place.name,
            "address": obj.place.address,
            "latitude": float(obj.place.latitude),
            "longitude": float(obj.place.longitude),
        }

class PlanFinalizeSerializer(serializers.Serializer):
    place_id = serializers.IntegerField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    note = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    def validate(self, attrs):
        if attrs["end_time"] <= attrs["start_time"]:
            raise serializers.ValidationError(
                "End time must be after start time."
            )

        return attrs