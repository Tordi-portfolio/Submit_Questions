from django.contrib import admin

from .models import (
    Question,
    StudentAnswer,
    StudentProgress,
    ExamSettings
)

admin.site.register(Question)
admin.site.register(StudentAnswer)
admin.site.register(StudentProgress)
admin.site.register(ExamSettings)