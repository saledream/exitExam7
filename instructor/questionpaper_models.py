from django.db import models
from django.forms import ModelForm
from .question_models import Question
from django import forms
from django.conf import settings 

User = settings.AUTH_USER_MODEL 

class Question_Paper(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    qPaperTitle = models.CharField(max_length=100)
    questions = models.ManyToManyField(Question) 

    def __str__(self):
        return f' Question Paper Title :- {self.qPaperTitle}\n'


class QPForm(ModelForm):
    def __init__(self,instructor,*args,**kwargs):
        super (QPForm,self ).__init__(*args,**kwargs) 
        self.fields['questions'].queryset = Question.objects.filter(instructor=instructor) 

    class Meta:
        model = Question_Paper
        fields = '__all__'
        exclude = ['instructor']
        widgets = {
            'qPaperTitle': forms.TextInput(attrs = {'class':'form-control'})
        }
