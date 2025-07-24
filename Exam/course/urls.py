from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.manage_courses, name='manage_courses'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
]