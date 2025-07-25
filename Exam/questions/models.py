from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from datetime import datetime
from .questionpaper_models import Question_Paper
from course.models import Course
from django import forms

class Exam_Model(models.Model):
    professor = models.ForeignKey(User, limit_choices_to={'groups__name': "Professor"}, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    name = models.CharField(max_length=50)
    total_marks = models.IntegerField()
    question_paper = models.ForeignKey(Question_Paper, on_delete=models.CASCADE, related_name='exams')
    start_time = models.DateTimeField(default=datetime.now())
    end_time = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.name


class ExamForm(ModelForm):
    def __init__(self, *args, **kwargs):
        professor = kwargs.pop('professor', None)
        course = kwargs.pop('course', None)
        super(ExamForm, self).__init__(*args, **kwargs)
        if course:
            self.fields['question_paper'].queryset = Question_Paper.objects.filter(
                professor=professor, course=course
            )

    class Meta:
        model = Exam_Model
        fields = '__all__'
        exclude = ['professor', 'course']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control'})
        }