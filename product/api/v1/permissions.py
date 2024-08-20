from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import Subscription


def make_payment(request):
    return Subscription.objects.filter(
        user=request.user.id
    ).exists()


class IsStudentOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        subscription_exists = Subscription.objects.filter(
            user=request.user.id
        ).exists()
        return (
            request.method in SAFE_METHODS and subscription_exists
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff


class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
