from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from rest_framework import serializers

from courses.models import Course, Group, Lesson

User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    """Список уроков."""

    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class CreateLessonSerializer(serializers.ModelSerializer):
    """Создание уроков."""

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class StudentSerializer(serializers.ModelSerializer):
    """Студенты курса."""

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class GroupSerializer(serializers.ModelSerializer):
    """Список групп."""

    students = StudentSerializer(source='users', many=True)

    class Meta:
        model = Group
        fields = (
            'title',
            'course',
            'students',
        )


class CreateGroupSerializer(serializers.ModelSerializer):
    """Создание групп."""

    class Meta:
        model = Group
        fields = (
            'title',
            'course',
        )


class MiniLessonSerializer(serializers.ModelSerializer):
    """Список названий уроков для списка курсов."""

    class Meta:
        model = Lesson
        fields = (
            'title',
        )


class CourseSerializer(serializers.ModelSerializer):
    """Список курсов."""

    lessons = MiniLessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField(read_only=True)
    students_count = serializers.SerializerMethodField(read_only=True)
    groups_filled_percent = serializers.SerializerMethodField(read_only=True)
    demand_course_percent = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj):
        """Количество уроков в курсе."""
        return obj.lessons.count()

    def get_students_count(self, obj):
        """Общее количество студентов на курсе."""
        return obj.subscriptions.count()

    def get_groups_filled_percent(self, obj):
        """Процент заполнения групп, если в группе максимум 30 чел.."""
        max_students = 30

        groups = obj.groups.annotate(
            count_students=(Count('users') * 100) / max_students
        )

        avg_filled = groups.aggregate(
            avg_filled=Avg('count_students')
        )['avg_filled']

        return avg_filled

    def get_demand_course_percent(self, obj):
        """Процент приобретения курса."""
        subscription_count = obj.subscriptions.count()
        total_users = User.objects.count()

        if total_users == 0:
            return 0

        demand_percent = (subscription_count / total_users) * 100
        return demand_percent

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'start_date',
            'price',
            'lessons_count',
            'lessons',
            'demand_course_percent',
            'students_count',
            'groups_filled_percent',
        )


class CreateCourseSerializer(serializers.ModelSerializer):
    """Создание курсов."""

    class Meta:
        model = Course
        fields = ()
