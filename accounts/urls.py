from django.urls import path
from .views import login_view, logout_view, register_view, dashboard

urlpatterns = [
    path('register/', register_view, name='register'),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
]