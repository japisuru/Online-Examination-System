from django.http import JsonResponse
from django.urls import reverse
import requests
import json
from .question_models import Question_DB
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.models import Group
from student.models import *
from django.utils import timezone
from student.models import StuExam_DB,StuResults_DB
from questions.questionpaper_models import QPForm
from questions.question_models import QForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from course.views import has_group
from course.models import Course

@login_required(login_url='faculty-login')
def view_exams_prof(request, course_id):
    course = get_object_or_404(Course, id=course_id, professor=request.user)
    prof = request.user
    
    if request.method == 'POST':
        form = ExamForm(request.POST, professor=prof, course=course)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.professor = prof
            exam.course = course
            exam.save()
            form.save_m2m()
            return redirect('view_exams', course_id=course.id)
    else:
        form = ExamForm(professor=prof, course=course)

    exams = Exam_Model.objects.filter(course=course)
    return render(request, 'exam/mainexam.html', {
        'exams': exams, 'examform': form, 'course': course
    })

@login_required(login_url='faculty-login')
def add_question_paper(request, course_id):
    course = get_object_or_404(Course, id=course_id, professor=request.user)
    
    if request.method == 'POST':
        form = QPForm(request.POST, course=course)
        if form.is_valid():
            paper = form.save(commit=False)
            paper.professor = request.user
            paper.course = course
            paper.save()
            form.save_m2m()
            return redirect('faculty-add_question_paper', course_id=course.id)
    else:
        form = QPForm(course=course)

    papers = Question_Paper.objects.filter(course=course)
    return render(request, 'exam/addquestionpaper.html', {
        'papers': papers, 'examform': form, 'course': course
    })

@login_required(login_url='faculty-login')
def add_questions(request, course_id):
    course = get_object_or_404(Course, id=course_id, professor=request.user)
    
    if request.method == 'POST':
        form = QForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.professor = request.user
            question.course = course
            question.save()
            return redirect('faculty-addquestions', course_id=course.id)
    else:
        form = QForm()
        
    return render(request, 'exam/addquestions.html', {
        'examform': form, 'course': course
    })

@login_required(login_url='faculty-login')
def question_bank(request, course_id):
    course = get_object_or_404(Course, id=course_id, professor=request.user)
    questions = Question_DB.objects.filter(course=course)
    return render(request, 'questions/question_bank.html', {'questions': questions, 'course': course})

@login_required(login_url='faculty-login')
def edit_question(request, course_id, qno):
    course = get_object_or_404(Course, id=course_id, professor=request.user)
    question = get_object_or_404(Question_DB, qno=qno, course=course)
    
    if request.method == 'POST':
        form = QForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question updated successfully!')
            return redirect('question_bank', course_id=course.id)
    else:
        form = QForm(instance=question)
        
    return render(request, 'questions/edit_question.html', {'form': form, 'course': course})

@login_required(login_url='faculty-login')
def delete_question(request, course_id, qno):
    course = get_object_or_404(Course, id=course_id, professor=request.user)
    question = get_object_or_404(Question_DB, qno=qno, course=course)
    
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question deleted successfully!')
        return redirect('question_bank', course_id=course.id)
        
    return render(request, 'questions/delete_question.html', {'question': question, 'course': course})

@login_required(login_url='faculty-login')
def view_previousexams_prof(request):
    prof = request.user
    student = 0
    try:
        exams = Exam_Model.objects.filter(professor=prof)
    except Exam_Model.DoesNotExist:
        exams = {}
    return render(request, 'exam/previousexam.html', {'exams': exams})

@login_required(login_url='login')
def student_view_previous(request):
    student = request.user
    
    # Get all completed exams for the student
    completed_student_exams = StuExam_DB.objects.filter(student=student, completed=1)
    
    # Extract the exam details
    list_of_completed = []
    for stu_exam in completed_student_exams:
        exam = stu_exam.qpaper.exams.first()  # Get the corresponding Exam_Model instance
        if exam:
            list_of_completed.append({
                'exam': exam,
                'score': stu_exam.score,
                'total_marks': exam.total_marks
            })

    # Data for charts
    exam_names = [item['exam'].name for item in list_of_completed]
    scores = [item['score'] for item in list_of_completed]
    total_marks = [item['total_marks'] for item in list_of_completed]

    # Calculate pass/fail
    pass_count = sum(1 for item in list_of_completed if (item['score'] / item['total_marks']) >= 0.4) # 40% pass mark
    fail_count = len(list_of_completed) - pass_count

    context = {
        'completed_exams': list_of_completed,
        'exam_names_json': json.dumps(exam_names),
        'scores_json': json.dumps(scores),
        'total_marks_json': json.dumps(total_marks),
        'pass_count': pass_count,
        'fail_count': fail_count,
    }
    return render(request, 'exam/previousstudent.html', context)

@login_required(login_url='faculty-login')
def view_students_prof(request):
    students = User.objects.filter(groups__name = "Student")
    student_name = []
    student_completed = []
    count = 0
    dicts = {}
    try:
        examn = Exam_Model.objects.filter(professor=request.user)
    except Exam_Model.DoesNotExist:
        examn = {}
    for student in students:
        for ex in examn:
            if StuExam_DB.objects.filter(student=student,examname=ex.name).exists():
                student_name.append(student.username)
                student_completed.append(ex.name)
    for i in student_name:
        if i not in dicts:
            dicts[i] = [student_completed[count]]
        else:
            dicts[i].append(student_completed[count])
        count+=1
    return render(request,'exam/viewstudents.html',{'students':dicts})

@login_required(login_url='faculty-login')
def view_results_prof(request):
    professor = request.user
    exams = Exam_Model.objects.filter(professor=professor)
    
    exam_stats = []
    total_pass = 0
    total_fail = 0

    for exam in exams:
        student_exams = StuExam_DB.objects.filter(examname=exam.name, completed=1)
        scores = [se.score for se in student_exams]
        
        if scores:
            average_score = sum(scores) / len(scores)
            pass_count = sum(1 for score in scores if (score / exam.total_marks) >= 0.4)
            fail_count = len(scores) - pass_count
            total_pass += pass_count
            total_fail += fail_count
            
            exam_stats.append({
                'name': exam.name,
                'average_score': average_score,
                'total_marks': exam.total_marks,
                'pass_count': pass_count,
                'fail_count': fail_count,
                'student_count': len(scores)
            })

    context = {
        'exam_stats': exam_stats,
        'exam_names_json': json.dumps([stat['name'] for stat in exam_stats]),
        'avg_scores_json': json.dumps([stat['average_score'] for stat in exam_stats]),
        'total_pass_json': json.dumps(total_pass),
        'total_fail_json': json.dumps(total_fail),
    }
    return render(request, 'exam/resultsstudent.html', context)

@login_required(login_url='login')
def view_exams_student(request):
    student = request.user
    enrolled_courses = student.enrolled_courses.all()
    exams = Exam_Model.objects.filter(course__in=enrolled_courses)
    
    list_of_completed = []
    list_un = []
    for exam in exams:
        try:
            stu_exam = StuExam_DB.objects.get(examname=exam.name, student=request.user)
            if stu_exam.completed == 1:
                list_of_completed.append(exam)
            else:
                list_un.append(exam)
        except StuExam_DB.DoesNotExist:
            list_un.append(exam)

    return render(request,'exam/mainexamstudent.html',{
        'exams':list_un,
        'completed':list_of_completed
    })

@login_required(login_url='login')
def view_students_attendance(request):
    exams = Exam_Model.objects.all()
    list_of_completed = []
    list_un = []
    for exam in exams:
        if StuExam_DB.objects.filter(examname=exam.name ,student=request.user).exists():
            if StuExam_DB.objects.get(examname=exam.name,student=request.user).completed == 1:
                list_of_completed.append(exam)
        else:
            list_un.append(exam)

    return render(request,'exam/attendance.html',{
        'exams':list_un,
        'completed':list_of_completed
    })

def convert(seconds): 
    min, sec = divmod(seconds, 60) 
    hour, min = divmod(min, 60) 
    min += hour*60
    return "%02d:%02d" % (min, sec) 

@login_required(login_url='login')
def appear_exam(request,id):
    student = request.user
    if request.method == 'GET':
        exam = Exam_Model.objects.get(pk=id)
        time_delta = exam.end_time - exam.start_time
        time = convert(time_delta.seconds)
        time = time.split(":")
        mins = time[0]
        secs = time[1]
        context = {
            "exam":exam,
            "question_list":exam.question_paper.questions.all(),
            "secs":secs,
            "mins":mins
        }
        return render(request,'exam/giveExam.html',context)
    if request.method == 'POST' :
        student = User.objects.get(username=request.user.username)
        paper = request.POST['paper']
        examMain = Exam_Model.objects.get(name = paper)
        stuExam = StuExam_DB.objects.get_or_create(examname=paper, student=student,qpaper = examMain.question_paper)[0]
        
        qPaper = examMain.question_paper
        stuExam.qpaper = qPaper
         
        qPaperQuestionsList = examMain.question_paper.questions.all()
        for ques in qPaperQuestionsList:
            student_question = Stu_Question(student=student,question=ques.question, optionA=ques.optionA, optionB=ques.optionB,optionC=ques.optionC, optionD=ques.optionD,
            answer=ques.answer)
            student_question.save()
            stuExam.questions.add(student_question)
            stuExam.save()

        stuExam.completed = 1
        stuExam.save()
        examQuestionsList = StuExam_DB.objects.filter(student=request.user,examname=paper,qpaper=examMain.question_paper,questions__student = request.user)[0]
        #examQuestionsList = stuExam.questions.all()
        examScore = 0
        list_i = examMain.question_paper.questions.all()
        queslist = examQuestionsList.questions.all()
        i = 0
        mark_per_question = 100 / list_i.count()
        for j in range(list_i.count()):
            ques = queslist[j]
            max_m = list_i[i].max_marks
            ans = request.POST.get(f'q{j}', False)
            if not ans:
                ans = "E"
            ques.choice = ans
            ques.save()
            answer = ques.answer
            # Build a mapping of options to their labels
            options = {
                "A": ques.optionA,
                "B": ques.optionB,
                "C": ques.optionC,
                "D": ques.optionD,
            }

            # Find which label matches the answer
            correct_choice = next((key for key, value in options.items() if value == answer), None)
            if ans.lower() == correct_choice.lower() or ans == correct_choice:
                examScore = examScore + (max_m * mark_per_question)
            i+=1

        stuExam.score = examScore
        stuExam.save()
        stu = StuExam_DB.objects.filter(student=request.user,examname=examMain.name)  
        results = StuResults_DB.objects.get_or_create(student=request.user)[0]
        results.exams.add(stu[0])
        results.save()
        result_url = reverse('result', args=[examMain.id])
        return JsonResponse({'success': True, 'result_url': result_url})

@login_required(login_url='login')
def result(request,id):
    student = request.user
    exam = Exam_Model.objects.get(pk=id)
    score = StuExam_DB.objects.get(student=student,examname=exam.name,qpaper=exam.question_paper).score
    return render(request,'exam/result.html',{'exam':exam,"score":score})

@login_required(login_url='login')
def review_exam(request, id):
    student = request.user
    exam = Exam_Model.objects.get(pk=id)
    stu_exam = StuExam_DB.objects.get(student=student, examname=exam.name, qpaper=exam.question_paper)
    
    student_questions = stu_exam.questions.all()
    original_questions = exam.question_paper.questions.all()
    
    review_data = []
    for i, sq in enumerate(student_questions):
        original_q = original_questions[i]
        options = {
            "A": {'text': sq.optionA, 'desc': original_q.descriptionA},
            "B": {'text': sq.optionB, 'desc': original_q.descriptionB},
            "C": {'text': sq.optionC, 'desc': original_q.descriptionC},
            "D": {'text': sq.optionD, 'desc': original_q.descriptionD},
        }
        correct_answer_text = sq.answer
        correct_choice = next((key for key, value in options.items() if value['text'] == correct_answer_text), None)

        review_data.append({
            'question_text': sq.question,
            'options': options,
            'student_choice': sq.choice,
            'correct_choice': correct_choice,
        })

    context = {
        'exam': exam,
        'review_data': review_data,
    }
    return render(request, 'exam/review_exam.html', context)

@login_required(login_url='faculty-login')
def add_questions_automatically(request, course_id):
    course = get_object_or_404(Course, id=course_id, professor=request.user)
    prof = request.user
    permissions = has_group(prof, "Professor")
    if not permissions:
        return redirect('view_exams_student')

    if request.method == 'POST':
        context = request.POST.get('context')
        number_of_questions = request.POST.get('number_of_questions')

        if context and number_of_questions:
            try:
                api_url = settings.API_URL
                payload = json.dumps({
                    "context": context,
                    "number_of_answers_for_questions": 4,
                    "number_of_questions": int(number_of_questions)
                })
                headers = {
                    'accept': 'application/json',
                    'x-api-key': settings.API_KEY,
                    'Content-Type': 'application/json'
                }
                response = requests.request("POST", api_url, headers=headers, data=payload)
                response.raise_for_status()
                data = response.json()

                if 'data' in data and 'questions' in data['data']:
                    for q_data in data.get('data', {}).get('questions', []):
                        answers = q_data.get('answers', [])
                        if len(answers) == 4:
                            correct_answer_text = ''
                            for ans in answers:
                                if ans.get('correct'):
                                    correct_answer_text = ans.get('text')
                                    break
                            
                            Question_DB.objects.create(
                                professor=prof,
                                course=course,
                                question=q_data.get('question_text'),
                                optionA=answers[0].get('text'),
                                optionB=answers[1].get('text'),
                                optionC=answers[2].get('text'),
                                optionD=answers[3].get('text'),
                                descriptionA=answers[0].get('description'),
                                descriptionB=answers[1].get('description'),
                                descriptionC=answers[2].get('description'),
                                descriptionD=answers[3].get('description'),
                                answer=correct_answer_text,
                                max_marks=1
                            )
                    messages.success(request, 'Questions generated successfully!')
                    return redirect('faculty-add-questions-auto', course_id=course.id)
                else:
                    messages.error(request, 'Failed to generate questions. Invalid API response.')

            except requests.exceptions.RequestException as e:
                messages.error(request, f"API request failed: {e}")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")

    return render(request, 'exam/add_questions_automatically.html', {'course': course})

