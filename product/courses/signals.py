from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Subscription
from courses.models import Group


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.

    """

    if created:
        groups_count = Group.objects.filter(course=instance.course).count()
        if groups_count < 3:
            Group.objects.create(
                title=f'Группа №{groups_count + 1}', course=instance.course
            )

        group = Group.objects.filter(course=instance.course).annotate(
            student_count=Count('users')
        ).order_by('student_count').first()

        group.users.add(instance.user)
