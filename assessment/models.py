from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.question_text[:50]
    


class StudentAnswer(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    answer = models.TextField()

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student.username} - {self.question}"
    


class StudentProgress(models.Model):

    student = models.OneToOneField(User, on_delete=models.CASCADE)

    current_index = models.IntegerField(default=0)

    completed = models.BooleanField(default=False)

    start_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.student.username
    


class ExamSettings(models.Model):
    duration_minutes = models.IntegerField(default=30)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.duration_minutes} mins"