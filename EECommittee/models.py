from django.db import models
from django.conf import settings 
from PIL import Image 
from io import BytesIO 
from django.core.files.uploadedfile import InMemoryUploadedFile 
import sys 
from django.urls import reverse 
from django.dispatch import receiver 
from django.db.models.signals import post_save 
from django.template.defaultfilters import slugify 
from django.utils.html import format_html 

User = settings.AUTH_USER_MODEL 

class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name 
    
    def _get_courses(self):
        url = '/admin/EECommittee/course/'
        
        return format_html(u'<a href="{}">{}</a>', 
                               url, self.courses.all().count())
    
    No_courses = property(_get_courses) 

    def _get_model_exams(self):
        url = '/admin/instructor/exam_model/'

        
        return format_html(u'<a href="{}">{}</a>', 
                               url, self.models.all().count()) 
    
    No_model_exams = property(_get_model_exams)

    def _get_instructor(self):
        url = '/admin/accounts/user/'

        
        return format_html(u'<a href="{}">{}</a>', 
                               url, self.users.filter(user_type="instructor").count()) 
    
    instructors = property(_get_instructor)  

    def _get_student(self):
        url = '/admin/accounts/user/'

        return format_html(u'<a href="{}">{}</a>', 
                               url, self.users.filter(user_type="student").count()) 
    
    students = property(_get_student)  

    
class Course(models.Model):
    name = models.CharField(max_length=255) 
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses") 
    description = models.TextField() 
    image = models.ImageField(upload_to="course_images") 
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses") 
    slug = models.SlugField(null=True, unique=True)  
    
    def __str__(self):
        return self.name 
   
    
    def get_absolute_url(self):
        return reverse("courses", kwargs={'slug':self.slug})
    
    
    def save(self, *args, **kwargs):
        

       
       self.slug = slugify(self.name) 
       super(Course,self).save(*args,**kwargs) 

       img = Image.open(self.image.path) 
       if img.height > 300 or img.width > 300:
           output_size = (288,200)
           img.thumbnail(output_size) 
           img.save(self.image.path)  

       
    def _get_module(self):
        url = '/admin/EECommittee/course/'
        
        return format_html(u'<a href="{}">{}</a>', 
                               url, self.modules.all().count())
       
    No_modules = property(_get_module) 

    def _get_tests(self):
        url = '/admin/EECommittee/course/'
        
        return format_html(u'<a href="{}">{}</a>', 
                               url, self.tests.all().count() )
       
    No_tests = property(_get_tests) 

    def _get_department(self):
        url = '/admin/EECommittee/department/'
        
        return format_html(u'<a href="{}">{}</a>', 
                               url, self.dept )
       
    department = property(_get_department) 


    

