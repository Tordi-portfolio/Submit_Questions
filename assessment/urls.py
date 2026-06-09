
from django.urls import path
from .views import (
    assessment_view,
    admin_questions,
    edit_question,
    delete_question,
    admin_responses
)

urlpatterns = [
    path('assessment_view/', assessment_view, name='assessment'),

    # ADMIN
    path('admin/questions/', admin_questions, name='admin_questions'),
    path('admin/questions/edit/<int:pk>/', edit_question, name='edit_question'),
    path('admin/questions/delete/<int:pk>/', delete_question, name='delete_question'),
    path('admin/responses/', admin_responses, name='admin_responses'),
]