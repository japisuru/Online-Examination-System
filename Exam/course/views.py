from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .models import Course

def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

@login_required(login_url='faculty-login')
def manage_courses(request):
    if not has_group(request.user, "Professor"):
        return redirect('view_exams_student')

    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        if course_name:
            Course.objects.create(name=course_name, professor=request.user)
        return redirect('manage_courses')

    courses = Course.objects.filter(professor=request.user)
    return render(request, 'course/manage_courses.html', {'courses': courses})

@login_required(login_url='faculty-login')
def course_detail(request, course_id):
    if not has_group(request.user, "Professor"):
        return redirect('view_exams_student')

    course = Course.objects.get(id=course_id, professor=request.user)
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        if student_id:
            student = User.objects.get(id=student_id)
            course.students.add(student)
        return redirect('course_detail', course_id=course.id)

    all_students = User.objects.filter(groups__name="Student")
    enrolled_students = course.students.all()
    unenrolled_students = all_students.exclude(id__in=enrolled_students.values_list('id', flat=True))

    return render(request, 'course/course_detail.html', {
        'course': course,
        'enrolled_students': enrolled_students,
        'unenrolled_students': unenrolled_students
    })
