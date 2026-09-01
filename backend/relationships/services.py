from django.contrib.auth.models import User

from .models import Relationship


def get_user_relationship(user: User):
    return (
        Relationship.objects
        .filter(members=user)
        .first()
    )