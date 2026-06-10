
from django.urls import path
from .views import (
    admin_users,
    assessment_view,
    admin_questions,
    edit_question,
    delete_question,
    admin_responses,
    exam_settings,
    user_responses,
    start_assessment,
)

urlpatterns = [
    path('', assessment_view, name='assessment'),

    # ADMIN
    path('admin/questions/', admin_questions, name='admin_questions'),
    path('admin/questions/edit/<int:pk>/', edit_question, name='edit_question'),
    path('admin/questions/delete/<int:pk>/', delete_question, name='delete_question'),
    path('admin/responses/', admin_responses, name='admin_responses'),

    path('admin/users/', admin_users, name='admin_users'),
    path('admin/users/<int:user_id>/', user_responses, name='user_responses'),

    path('admin/settings/', exam_settings, name='exam_settings'),

    path('start-assessment/', start_assessment, name='start_assessment'),
]