from django.urls import path
from .views import student_results, student_result_pdf

urlpatterns = [
    path('student/<int:student_id>/results/', student_results, name='student_results'),
    path('student/<int:student_id>/results/pdf/', student_result_pdf, name='student_result_pdf'),
]
