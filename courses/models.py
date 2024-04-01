from django.db import models
from django.contrib.auth.models import User 
from django.conf import settings 



User = settings.AUTH_USER_MODEL 
# Create your models here. 
class Department(models.Model):
    name = models.CharField(max_length=20, unique=True)  

    def __str__(self):
        return self.name 

class Course(models.Model):
    name = models.CharField(max_length=20) 
    dep_id = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses") 
    description = models.TextField() 
    exitexiam_guideline = models.TextField() 
    image = models.ImageField(upload_to="course_images") 
    instructors = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses") 
    

class Module(models.Model):

    name = models.CharField(max_length=255) 
    description = models.TextField() 
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules") 
    author_name = models.ForeignKey(User, on_delete=models.CASCADE,related_name="modules") 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)


class  Section(models.Model):
    title = models.CharField(max_length=255) 
    notes = models.TextField() 
    image = models.ImageField(blank=True, null=True, upload_to="section_images") 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="sections") 


class Test(models.Model):
    
    diff_level = (
        ('hard','hard'),
        ('medium','medium'),
        ('easy','easy')
    )
    exam_name = models.CharField(max_length=255) 
    question = models.TextField() 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    author_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tests") 
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="test") 
    difficulty = models.CharField(max_length=255, choices=diff_level)

class ModelExam(models.Model):
    
    diff_level = (
        ('hard','hard'),
        ('medium','medium'),
        ('easy','easy')
    )
    exam_name = models.CharField(max_length=255) 
    question = models.TextField() 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    author_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="model") 
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="model") 
    difficulty = models.CharField(max_length=255, choices=diff_level)
    


