from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import Subscription

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""
    bonus = serializers.IntegerField(source='balance.bonus')

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'bonus'
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""
    course = serializers.CharField(source='course.title')

    class Meta:
        model = Subscription
        fields = (
            'course', 'active'
        )
