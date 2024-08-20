from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    group = models.ForeignKey(
        'courses.Group',
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Группа',
        related_name='users',
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            Balance.objects.get_or_create(user=self)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя."""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='balance',
    )
    bonus = models.PositiveIntegerField(
        default=1000,
        verbose_name='Бонусы',
    )

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='subscriptions',
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        verbose_name='Курс',
        related_name='subscriptions',
    )
    active = models.BooleanField(
        default=True,
        verbose_name='Активна ли подписка',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)
