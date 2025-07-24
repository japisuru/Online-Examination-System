from django.http import JsonResponse
from django.urls import reverse
import requests
import json
from .question_models import Question_DB
from django.shortcuts import render,redirect
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

@login_required(login_url='faculty-login')
def view_exams_prof(request):
    prof = request.user
    prof_user = User.objects.get(username=prof)
    permissions = False
    if prof:
        permissions = has_group(prof,"Professor")
    if permissions:
        new_Form = ExamForm(prof_user)
        if request.method == 'POST' and permissions:
            form = ExamForm(prof_user,request.POST)
            if form.is_valid():
                exam = form.save(commit=False)
                exam.professor = prof
                exam.save()
                form.save_m2m()
                return redirect('view_exams')

        try:
            exams = Exam_Model.objects.filter(professor=prof)
        except Exam_Model.DoesNotExist:
            exams = {}
        return render(request, 'exam/mainexam.html', {
            'exams': exams, 'examform': new_Form, 'prof': prof,
        })
    else:
        return redirect('view_exams_student')

@login_required(login_url='faculty-login')
def add_question_paper(request):
    prof = request.user
    prof_user = User.objects.get(username=prof)
    permissions = False
    if prof:
        permissions = has_group(prof,"Professor")
    if permissions:
        new_Form = QPForm(prof_user)
        if request.method == 'POST' and permissions:
            form = QPForm(prof_user,request.POST)
            if form.is_valid():
                exam = form.save(commit=False)
                exam.professor = prof_user
                exam.save()
                form.save_m2m()
                return redirect('faculty-add_question_paper')

        try:
            exams = Exam_Model.objects.filter(professor=prof)
        except Exam_Model.DoesNotExist:
            exams = {}
        return render(request, 'exam/addquestionpaper.html', {
            'exams': exams, 'examform': new_Form, 'prof': prof,
        })
    else:
        return redirect('view_exams_student')

@login_required(login_url='faculty-login')
def add_questions(request):
    prof = request.user
    prof_user = User.objects.get(username=prof)
    permissions = False
    if prof:
        permissions = has_group(prof,"Professor")
    if permissions:
        new_Form = QForm()
        if request.method == 'POST' and permissions:
            form = QForm(request.POST)
            if form.is_valid():
                exam = form.save(commit=False)
                exam.professor = prof_user
                exam.save()
                form.save_m2m()
                return redirect('faculty-addquestions')

        try:
            exams = Exam_Model.objects.filter(professor=prof)
        except Exam_Model.DoesNotExist:
            exams = {}
        return render(request, 'exam/addquestions.html', {
            'exams': exams, 'examform': new_Form, 'prof': prof,
        })
    else:
        return redirect('view_exams_student')

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
    exams = Exam_Model.objects.all()
    list_of_completed = []
    list_un = []
    for exam in exams:
        if StuExam_DB.objects.filter(examname=exam.name ,student=request.user).exists():
            if StuExam_DB.objects.get(examname=exam.name,student=request.user).completed == 1:
                list_of_completed.append(exam)
        else:
            list_un.append(exam)

    return render(request,'exam/previousstudent.html',{
        'exams':list_un,
        'completed':list_of_completed
    })

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
    students = User.objects.filter(groups__name = "Student")
    dicts = {}
    prof = request.user
    professor = User.objects.get(username=prof.username)
    try:
        examn = Exam_Model.objects.filter(professor=professor)
    except Exam_Model.DoesNotExist:
        examn = {}
    for student in students:
        for ex in examn:
            if StuExam_DB.objects.filter(student=student,examname=ex.name).exists():
                score = StuExam_DB.objects.get(student=student,examname=ex.name).score
                if student.username not in dicts:
                    dicts[student.username] = [score]
                else:
                    dicts[student.username].append(score)
    return render(request,'exam/resultsstudent.html',{'students':dicts})

@login_required(login_url='login')
def view_exams_student(request):
    student = request.user
    enrolled_courses = student.enrolled_courses.all()
    exams = Exam_Model.objects.filter(course__in=enrolled_courses)
    
    list_of_completed = []
    list_un = []
    for exam in exams:
        if StuExam_DB.objects.filter(examname=exam.name ,student=request.user).exists():
            if StuExam_DB.objects.get(examname=exam.name,student=request.user).completed == 1:
                list_of_completed.append(exam)
        else:
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

from django.conf import settings
from django.contrib import messages

@login_required(login_url='faculty-login')
def add_questions_automatically(request):
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
                print("settings.API_URL: " + settings.API_URL)
                payload = json.dumps({
                    "context": context,
                    "number_of_answers_for_questions": 4,
                    "number_of_questions": int(number_of_questions)
                })
                print("settings.API_KEY: " + settings.API_KEY)
                headers = {
                    'accept': 'application/json',
                    'x-api-key': settings.API_KEY,
                    'Content-Type': 'application/json'
                }
                response = requests.request("POST", api_url, headers=headers, data=payload)
                response.raise_for_status()  # Raise an exception for bad status codes
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
                                question=q_data.get('question_text'),
                                optionA=answers[0].get('text'),
                                optionB=answers[1].get('text'),
                                optionC=answers[2].get('text'),
                                optionD=answers[3].get('text'),
                                answer=correct_answer_text,
                                max_marks=1
                            )
                    messages.success(request, 'Questions generated successfully!')
                    return redirect('faculty-add-questions-auto')
                else:
                    messages.error(request, 'Failed to generate questions. Invalid API response.')

            except requests.exceptions.RequestException as e:
                messages.error(request, f"API request failed: {e}")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")

    return render(request, 'exam/add_questions_automatically.html')