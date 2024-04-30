from django.contrib import admin

from .models import TinyGroup, RichGroup, DaySchedule, Lesson, Stats, Homework

admin.site.register(TinyGroup)
admin.site.register(RichGroup)
admin.site.register(DaySchedule)
admin.site.register(Lesson)
admin.site.register(Stats)
admin.site.register(Homework)
