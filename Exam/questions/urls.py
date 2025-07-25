from django.urls import path
from . import views

urlpatterns = [
    # Student URLs
    path('student/viewexams/', views.view_exams_student, name="view_exams_student"),
    path('student/previous/', views.student_view_previous, name="student-previous"),
    path('student/appear/<int:id>', views.appear_exam, name="appear-exam"),
    path('student/result/<int:id>', views.result, name="result"),
    path('student/review/<int:id>/', views.review_exam, name='review_exam'),
    path('student/review/<int:id>/pdf/', views.review_exam_pdf, name="review_exam_pdf"),
    path('student/attendance/', views.view_students_attendance, name="view_students_attendance"),

    # Professor URLs (now course-specific)
    path('course/<int:course_id>/exams/', views.view_exams_prof, name="view_exams"),
    path('course/<int:course_id>/question-bank/', views.question_bank, name='question_bank'),
    path('course/<int:course_id>/add-question/', views.add_questions, name='faculty-addquestions'),
    path('course/<int:course_id>/add-question-paper/', views.add_question_paper, name='faculty-add_question_paper'),
    path('course/<int:course_id>/add-questions-auto/', views.add_questions_automatically, name='faculty-add-questions-auto'),
    path('course/<int:course_id>/question/<int:qno>/edit/', views.edit_question, name='edit_question'),
    path('course/<int:course_id>/question/<int:qno>/delete/', views.delete_question, name='delete_question'),
    
    # General Professor URLs (not course-specific)
    path('prof/viewpreviousexams/', views.view_previousexams_prof, name="faculty-previous"),
    path('prof/viewresults/', views.view_results_prof, name="faculty-result"),
    path('prof/viewstudents/', views.view_students_prof, name="faculty-student"),
]
