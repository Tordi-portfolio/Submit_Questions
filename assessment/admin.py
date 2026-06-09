from django.contrib import admin

from .models import (
    Question,
    StudentAnswer,
    StudentProgress
)

admin.site.register(Question)
admin.site.register(StudentAnswer)
admin.site.register(StudentProgress)