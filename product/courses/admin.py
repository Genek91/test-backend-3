from django.contrib import admin

from courses.models import Course, Lesson, Group
from users.models import CustomUser, Balance

admin.site.register(CustomUser)
admin.site.register(Balance)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Group)
