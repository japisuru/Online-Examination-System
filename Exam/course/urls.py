from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.manage_courses, name='manage_courses'),
    path('<int:course_id>/', views.course_dashboard, name='course_dashboard'),
    path('<int:course_id>/students/', views.course_detail, name='course_detail'),
]