from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course
from users.models import Subscription


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""
        course = get_object_or_404(Course, pk=pk)
        balance = request.user.balance

        if balance.bonus < course.price:
            return Response(
                'Недостаточно бонусов',
                status=status.HTTP_400_BAD_REQUEST
            )

        subscription, created = Subscription.objects.get_or_create(
            user=request.user, course=course
        )
        if not created:
            return Response(
                'Подписка уже оформлена',
                status=status.HTTP_400_BAD_REQUEST
            )

        balance.bonus -= course.price
        balance.save()

        return Response(
            data=SubscriptionSerializer(subscription).data,
            status=status.HTTP_201_CREATED
        )

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def available(self, request):
        available_courses = Course.objects.exclude(
            subscriptions__user=request.user
        ).all()
        return Response(
            data=CourseSerializer(available_courses, many=True).data,
            status=status.HTTP_200_OK
        )
