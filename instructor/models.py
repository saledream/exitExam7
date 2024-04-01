from django.db import models
from django.contrib.humanize.templatetags import humanize 
from tinymce.models import HTMLField 
from ckeditor_uploader.fields import RichTextUploadingField 
from django.conf import settings 
from EECommittee.models import Course, Department  
from django.forms import ModelForm
from django.utils import timezone 
from django import forms
from django.utils.safestring import mark_safe 
from django.template.defaultfilters import slugify 
from django.urls import reverse 
from django.utils.html import format_html 

User = settings.AUTH_USER_MODEL 

class Module(models.Model):

    name = models.CharField(max_length=255) 
    overview = RichTextUploadingField() 
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules") 
    instructor = models.ForeignKey(User, on_delete=models.CASCADE,related_name="modules") 
    created_date = models.DateTimeField(auto_now_add=True) 
    updated_date = models.DateTimeField(auto_now=True) 
    
    def save(self,*args, **kwargs):

        self.overview = mark_safe(self.overview) 

        super().save(*args,**kwargs) 
    def get_created_date(self):
        return humanize.naturaltime(self.created_date) 
    
    def get_updated_date(self):
        return humanize.naturaltime(self.updated_date) 
    
    def __str__(self) -> str:
          return self.name 
    
    def _get_pages(self):
        url = '/admin/instructor/page/'

        return format_html(u'<a href="{}">{}</a>', 
                               url, self.pages.all().count())
    
    No_pages = property(_get_pages) 

    def _get_module_update_date(self):

        return humanize.naturaltime(self.updated_date) 
    
    updated = property(_get_module_update_date) 

    

class Page(models.Model):
    title = models.CharField(max_length=255) 
    notes = RichTextUploadingField()
    created_date = models.DateTimeField(auto_now_add=True) 
    updated_date = models.DateTimeField(auto_now=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="pages") 
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pages') 
    completionQuestion = models.CharField(max_length=255) 
    completionQuestionAns = models.CharField(max_length=255) 
    answerHint = models.CharField(max_length=255) 
    noteStatus = models.CharField(max_length=255, choices=(('drafted','drafted'),('published','published'))) 

        
    def save(self,*args, **kwargs):

        self.notes = mark_safe(self.notes) 

        super().save(*args,**kwargs) 

    def __str__(self) -> str:
        return self.title 
    
    def get_created_date(self):
        return humanize.naturaltime(self.created_date) 
    
    def get_updated_date(self):
        return humanize.naturaltime(self.updated_date) 
    
    def _get_modules(self):
        url = '/admin/EECommittee/department'
        
        return format_html(u'<a href="{}">{}</a>', 
                               url, self.module)
    
    modules = property(_get_modules) 

    def _get_module_update_date(self):

        return humanize.naturaltime(self.updated_date) 
    
    updated = property(_get_module_update_date) 
    

class PageCompletion(models.Model):

    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='completed_page') 
    student = models.ForeignKey(User,on_delete=models.CASCADE, related_name='completed_page')
    completion_date = models.DateTimeField(auto_now_add=True)

    def _get_completion_date(self):
        return humanize.naturaltime(self.completion_date) 
    
    completed_date = property(_get_completion_date)

    def _get_deparment(self):

        return self.student.department 
    
    department = property(_get_deparment) 

    def _get_cppage(self):

        return self.page  
    
    completed_page =  property(_get_cppage) 
    
    def _get_module(self):

        return self.page.module   
    
    module =  property(_get_module)

    def _get_course(self):

        return self.page.module.course   
    
    course =  property(_get_course)   
  


class Exam_Model(models.Model):
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="models") 
    title = models.CharField(max_length=50)
    

    def __str__(self):
        return self.title 
    
    def _get_questions(self):

        return self.question.all().count() 
    
    questions = property(_get_questions) 
    

class Test(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="tests") 
    instructor = models.ForeignKey(User, on_delete=models.CASCADE,related_name="tests", null=True)
     
    title = models.CharField(max_length=50)
    slug = models.SlugField(null=True)  
    
    def _get_questions(self):

        return self.test.all().count() 
    
    questions =  property(_get_questions) 

    def __str__(self):
        return self.title 
    
    def get_absolute_url(self):
        return reverse("test_detail", kwargs={'slug':self.slug})
    
    def save(self,*args,**kwargs):
        
        ctime = str(timezone.now())
        
        if not self.slug:

            self.slug = slugify(self.title+ ctime)  
        
        return super().save(*args,**kwargs) 
    

class ModelExamForm(ModelForm):
   
    class Meta:
        model = Exam_Model
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs = {'class':'form-control'}),
        }

class TestForm(ModelForm):
    class Meta:
        model = Test 
        fields = '__all__'
        


class ExamResult(models.Model):
    

    exam = models.ForeignKey(Exam_Model, on_delete=models.CASCADE, related_name='results') 
    score = models.IntegerField(default=0) 
    student = models.ForeignKey(User, on_delete=models.CASCADE,related_name='exam_result')
    exam_type = models.CharField(max_length=20)
    total_mark = models.PositiveIntegerField() 

    def save(self,*args, **kwargs):
        if self.exam_type == "model":
            self.total_mark = self.exam.question.all().count() 

        elif self.exam_type == "test":
             self.total_mark = self.exam.test.all().count() 

        super().save(*args,**kwargs) 


class CourseProgress(models.Model):

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="course_progress") 
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="progress") 
    progress = models.PositiveIntegerField(default=0) 
    
    def _get_department(self):

        return self.student.department 
    
    department = property(_get_department) 

   
class ModelQuestion(models.Model):
      q_type_opions = (
          ('hard','hard'),
          ('medium','medium'),
          ('easy','easy')
      )
      modeExam = models.ForeignKey(Exam_Model, on_delete=models.CASCADE,related_name="question")
      instructor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
      qno = models.AutoField(primary_key=True)
      question = RichTextUploadingField()
      optionA = models.CharField(max_length=255)
      optionB = models.CharField(max_length=255)
      optionC = models.CharField(max_length=255)
      optionD = models.CharField(max_length=255)
      optionA_slug = models.SlugField() 
      optionB_slug = models.SlugField() 
      optionC_slug = models.SlugField() 
      optionD_slug = models.SlugField() 

      answer = models.CharField(max_length=255)
      ans_description = models.TextField()
      question_type = models.CharField(max_length=255, choices=q_type_opions) 
      
      def save(self, *args, **kwargs):


        self.question = format_html(self.question) 
        self.optionA_slug = slugify(self.optionA) 
        self.optionB_slug = slugify(self.optionB) 
        self.optionC_slug = slugify(self.optionC) 
        self.optionD_slug = slugify(self.optionD) 

        super().save(*args,**kwargs)
    
      def question_field(self):
        text = ""
        if len(self.question) > 30:
           text = self.question[:30] + " ..."

        else:
            text = self.question    

        return mark_safe(text)

      def answer_field(self):
        text = ""
        if len(self.answer) > 30:
           text = self.answer[:30] + " ..."

        else:
            text = self.answer    

        return mark_safe(text)
      def ans_description_field(self):
        text = ""
        if len(self.ans_description) > 30:
           text = self.ans_description[:30] + " ..."

        else:
            text = self.ans_description    

        return mark_safe(text)
      
class TestQuestion(models.Model):
      q_type_opions = (
          ('hard','hard'),
          ('medium','medium'),
          ('easy','easy')
      )
      testExam = models.ForeignKey(Test, on_delete=models.CASCADE,related_name="test")
      instructor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
      qno = models.AutoField(primary_key=True)
      question = RichTextUploadingField()
      optionA = models.CharField(max_length=255)
      optionB = models.CharField(max_length=255)
      optionC = models.CharField(max_length=255)
      optionD = models.CharField(max_length=255)
      answer = models.CharField(max_length=255)
      optionA_slug = models.SlugField(unique=True) 
      optionB_slug = models.SlugField(unique=True) 
      optionC_slug = models.SlugField(unique=True) 
      optionD_slug = models.SlugField(unique=True) 
      question_type = models.CharField(max_length=255, choices=q_type_opions) 
      ans_description = models.TextField()
   
      def save(self, *args, **kwargs):
            
            self.question = format_html(self.question)
            c_time = str(timezone.now()) 
            self.optionA_slug = slugify(self.optionA + c_time) 

            c_time = str(timezone.now()) 
            self.optionB_slug = slugify(self.optionB + c_time) 

            c_time = str(timezone.now()) 
            self.optionC_slug = slugify(self.optionC + c_time) 

            c_time = str(timezone.now()) 
            self.optionD_slug = slugify(self.optionD + c_time) 
            super().save(*args,**kwargs)

      def __str__(self):
            return self.question  
    
      def question_field(self):
            text = ""
            if len(self.question) > 30:
                 text = self.question[:30] + " ..."

            else:
                text = self.question    

            return mark_safe(text)

      def answer_field(self):
            text = ""
            if len(self.answer) > 30:
                 text = self.answer[:30] + " ..."

            else:
                text = self.answer    

            return mark_safe(text)
      def ans_description_field(self):
            text = ""
            if len(self.ans_description) > 30:
                text = self.ans_description[:30] + " ..."

            else:
                text = self.ans_description    

            return mark_safe(text)

class ExamStatus(models.Model):
 student = models.ForeignKey(User, on_delete=models.CASCADE,related_name='exam_status') 
 question = models.ForeignKey(ModelQuestion,on_delete=models.CASCADE,related_name='exam_status')
 response = models.CharField(max_length=255)  
 response_status = models.CharField(max_length=255) 
 question_category = models.CharField(max_length=255) 
 category_name     = models.CharField(max_length=255) 
 department = models.ForeignKey(Department, on_delete=models.CASCADE,related_name="examstatus")


 def save(self,*args,**kwargs):
     
     self.response = self.response.replace("-"," ")
     self.department = self.student.department 
     if slugify(self.response) == slugify(self.question.answer):
         self.response_status = "correct"

     else:
         self.response_status = "wrong"  
     
     try:
        self.category_name = self.question.testExam.title
        self.question_catefory = "test"
     except AttributeError:
        self.question_catefory = 'model' 
        self.category_name = self.question.modeExam.title
     
     super().save(*args,**kwargs)

class ModelQuestionForm(ModelForm):
      class Meta:
        model = ModelQuestion
        fields = "__all__" 
        exclude = ['qno']  

class TestQuestionForm(ModelForm):
    class Meta:
        model = ModelQuestion
        fields = "__all__" 
        exclude = ['qno']  