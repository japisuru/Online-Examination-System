from django.shortcuts import render,redirect
from django.views import View
from .forms import StudentForm, StudentInfoForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode 
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .utils import account_activation_token
from django.core.mail import EmailMessage
import threading
import json
from django.contrib.auth.models import User
from studentPreferences.models import StudentPreferenceModel
from django.contrib.auth.models import Group
from questions.models import Exam_Model
from student.models import StuExam_DB

@login_required(login_url='login')
def index(request):
    student = request.user
    enrolled_courses = student.enrolled_courses.all()
    all_exams = Exam_Model.objects.filter(course__in=enrolled_courses).order_by('start_time')
    
    completed_exams_qset = StuExam_DB.objects.filter(student=student, completed=1).order_by('-id')
    completed_exams_list = [item.examname for item in completed_exams_qset]

    # Performance Trend Data
    list_of_completed_for_chart = []
    for stu_exam in completed_exams_qset.reverse(): # Reverse for chronological order in chart
        exam_model = all_exams.filter(name=stu_exam.examname).first()
        if exam_model:
            list_of_completed_for_chart.append({
                'exam': exam_model,
                'score': stu_exam.score,
                'total_marks': exam_model.total_marks
            })

    exam_names = [item['exam'].name for item in list_of_completed_for_chart]
    scores = [item['score'] for item in list_of_completed_for_chart]
    total_marks = [item['total_marks'] for item in list_of_completed_for_chart]
    
    percentages = []
    for i in range(len(scores)):
        if total_marks[i] > 0:
            percentages.append((scores[i] / total_marks[i]) * 100)
        else:
            percentages.append(0)

    # Widgets Data
    upcoming_exams = all_exams.exclude(name__in=completed_exams_list)[:3]
    latest_result = completed_exams_qset.first()
    latest_exam_model = None
    if latest_result:
        latest_exam_model = all_exams.filter(name=latest_result.examname).first()

    total_score = sum(scores)
    average_score = (total_score / len(scores)) if scores else 0
    
    context = {
        'exam_names_json': json.dumps(exam_names),
        'percentages_json': json.dumps(percentages),
        'has_completed_exams': len(list_of_completed_for_chart) > 0,
        'upcoming_exams': upcoming_exams,
        'latest_result': latest_result,
        'latest_exam_model': latest_exam_model,
        'average_score': average_score,
        'courses_enrolled_count': enrolled_courses.count(),
        'exams_completed_count': len(list_of_completed_for_chart),
    }
    return render(request,'student/index.html', context)

class Register(View):
    def get(self,request):
        student_form = StudentForm()
        student_info_form = StudentInfoForm()
        return render(request,'student/register.html',{'student_form':student_form,'student_info_form':student_info_form})
    
    def post(self,request):
        student_form = StudentForm(data=request.POST)
        student_info_form = StudentInfoForm(data=request.POST)
        email = request.POST['email']

        if student_form.is_valid() and student_info_form.is_valid():
            student = student_form.save()
            student.set_password(student.password)
            student.is_active = False
            my_group = Group.objects.get_or_create(name='Student')
            my_group[0].user_set.add(student)
            student.save()

            uidb64 = urlsafe_base64_encode(force_bytes(student.pk))
            domain = get_current_site(request).domain
            link = reverse('activate',kwargs={'uidb64':uidb64,'token':account_activation_token.make_token(student)})
            activate_url = 'http://' + domain +link
            email_subject = 'Activate your Exam Portal account'
            email_body = 'Hi.Please use this link to verify your account\n' + activate_url + ".\n\n You are receiving this message because you registered on " + domain +". If you didn't register please contact support team on " + domain 
            fromEmail = 'noreply@exam.com'
            email = EmailMessage(
				email_subject,
				email_body,
				fromEmail,
				[email],
            )
            student_info = student_info_form.save(commit=False)
            student_info.user = student
            if 'picture' in request.FILES:
                student_info.picture = request.FILES['picture']
            student_info.save()
            messages.success(request,"Registered Succesfully. Check Email for confirmation")
            EmailThread(email).start()
            return redirect('login')
        else:
            print(student_form.errors,student_info_form.errors)
            return render(request,'student/register.html',{'student_form':student_form,'student_info_form':student_info_form})
    
class LoginView(View):
	def get(self,request):
		return render(request,'student/login.html')
	def post(self,request):
		username = request.POST['username']
		password = request.POST['password']

		if username and password:
			exis = User.objects.filter(username=username).exists()
			if exis:
				user_ch = User.objects.get(username=username)
				if user_ch.is_staff:
					messages.error(request,"You are trying to login as student, but you have registered as faculty. We are redirecting you to faculty login. If you are having problem in logging in please reset password or contact admin")
					return redirect('faculty-login')
			user = auth.authenticate(username=username,password=password)
			if user:
				if user.is_active:
					auth.login(request,user)
					student_pref = StudentPreferenceModel.objects.filter(user = request.user).exists()
					email = User.objects.get(username=username).email

					email_subject = 'You Logged into your Portal account'
					email_body = "If you think someone else logged in. Please contact support or reset your password.\n\nYou are receving this message because you have enabled login email notifications in portal settings. If you don't want to recieve such emails in future please turn the login email notifications off in settings."
					fromEmail = 'noreply@exam.com'
					email = EmailMessage(
						email_subject,
						email_body,
						fromEmail,
						[email],
					)
					if student_pref :
						student = StudentPreferenceModel.objects.get(user=request.user)
						sendEmail = student.sendEmailOnLogin 
					if not student_pref :
						EmailThread(email).start()
					elif sendEmail:
						EmailThread(email).start()
					messages.success(request,"Welcome, "+ user.username + ". You are now logged in.")

					return redirect('index')
			
			else:
				user_n = User.objects.filter(username=username).exists()
				if user_n:
					user_v = User.objects.get(username=username)
					if user_v.is_active:
						messages.error(request,'Invalid credentials')	
						return render(request,'student/login.html')
					else:
						messages.error(request,'Account not Activated')
						return render(request,'student/login.html')

		messages.error(request,'Please fill all fields')
		return render(request,'student/login.html')

class LogoutView(View):
	def post(self,request):
		auth.logout(request)
		messages.success(request,'Logged Out')
		return redirect('login')

class EmailThread(threading.Thread):
	def __init__(self,email):
		self.email = email
		threading.Thread.__init__(self)

	
	def run(self):
		self.email.send(fail_silently = False)

class VerificationView(View):
	def get(self,request,uidb64,token):
		try:
			id = force_text(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=id)
			if not account_activation_token.check_token(user,token):
				messages.error(request,"User already Activated. Please Proceed With Login")
				return redirect("login")
			if user.is_active:
				return redirect('login')
			user.is_active = True
			user.save()
			messages.success(request,'Account activated Sucessfully')
			return redirect('login')
		except Exception as e:
			raise e
		return redirect('login')
	