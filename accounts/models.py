from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.humanize.templatetags import humanize 
from django.forms import ModelForm 
from .manager import CustomUserManager
from EECommittee.models import Department 


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('student','Student'),
        ('instructor','Instructor'),
        ('admin','admin'), 
    )
    user_type = models.CharField(max_length=20,choices=USER_TYPE_CHOICES,default='student') 
    first_name = models.CharField(max_length=255,null=True, blank=True) 
    last_name = models.CharField(max_length=255, null=True, blank=True) 
    username = models.CharField(max_length=255,unique=True) 
    email = models.EmailField(_("email"), unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,related_name='users', null=True)
    avtar = models.ImageField(null=True, blank=True,upload_to='profile_picture') 
    bio   = models.CharField(max_length=255, blank=True, null=True)  
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
  
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.username or self.email.split('@')[0]
    
    def is_admin(self):
        return self.user_type == 'admin' 
    
    def is_student(self):
        return self.user_type == 'student' 
    
    def is_instructor(self):
        return self.user_type == 'instructor' 
    
    def _get_login_date(self):

        return humanize.naturaltime(self.date_joined) 
    
    joined_date = property(_get_login_date) 

    def _get_last_seen_date(self):

        return humanize.naturaltime(self.last_login) 
    
    last_seen = property(_get_last_seen_date) 

    def _get_course_progress(self):
        from instructor.models import CourseProgress 
        completed = 0
        for cp in CourseProgress.objects.filter(student__username=self.username):
            
            if cp.progress == 100:
                completed += 1
            
        return completed 
    
    completed_course = property(_get_course_progress) 
    
    
    
class SuperUserForm(ModelForm):

    class Meta:
        model = User
        fields = "__all__"  

class NormalUserForm(ModelForm):
    
    class Meta:
        model = User 
        fields = ['username','first_name','last_name','email','department','avtar','bio']

# class Admin(User):

#     class Meta:
#         proxy = True 

# class StudentManager(models.Manager):

#     def get_queryset(self,*args,**kwargs) -> models.QuerySet:
#         return super().get_queryset(*args,**kwargs).filter(user_type='student')  
 
# class Student(User):
    
#     objects = StudentManager()
#     class Meta:
#         proxy = True 


# class InstructorManager(models.Manager):

#     def get_queryset(self,*args,**kwargs) -> models.QuerySet:
#         return super().get_queryset(*args,**kwargs).filter(user_type='instructor')  
    
    
# class Instructor(User):

#     objects = InstructorManager()
#     class Meta:
#         proxy = True 


# class Department(models.Model):
#     name = models.CharField(max_length=20, unique=True)  

#     def __str__(self):
#         return self.name 

# class Course(models.Model):
#     name = models.CharField(max_length=20) 
#     dep_id = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses") 
#     description = models.TextField() 
#     exitexiam_guideline = models.TextField() 
#     image = models.ImageField(upload_to="course_images") 
#     instructors = models.ForeignKey(User, on_delete=models.CASCADE, related_name="instructor") 


# class Module(models.Model):

#     name = models.CharField(max_length=255) 
#     description = models.TextField() 
#     course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules") 
#     # instructor = models.ForeignKey(User, on_delete=models.CASCADE,related_name="instructor") 
#     created = models.DateTimeField(auto_now_add=True) 
#     updated = models.DateTimeField(auto_now=True)


# class  Section(models.Model):
#     title = models.CharField(max_length=255) 
#     notes = models.TextField() 
#     image = models.ImageField(blank=True, null=True, upload_to="section_images") 
#     created = models.DateTimeField(auto_now_add=True) 
#     updated = models.DateTimeField(auto_now=True)
#     module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="pages") 


# class Test(models.Model):
    
#     diff_level = (
#         ('hard','hard'),
#         ('medium','medium'),
#         ('easy','easy')
#     )
#     exam_name = models.CharField(max_length=255) 
#     question = models.TextField() 
#     created = models.DateTimeField(auto_now_add=True) 
#     updated = models.DateTimeField(auto_now=True) 
#     instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="instructor") 
#     module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="tests") 
#     difficulty = models.CharField(max_length=255, choices=diff_level)

# class ModelExam(models.Model):
    
#     diff_level = (
#         ('hard','hard'),
#         ('medium','medium'),
#         ('easy','easy')
#     )
#     exam_name = models.CharField(max_length=255) 
#     question = models.TextField() 
#     created = models.DateTimeField(auto_now_add=True) 
#     updated = models.DateTimeField(auto_now=True) 
#     instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="instructor") 
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modelExam") 
#     difficulty = models.CharField(max_length=255, choices=diff_level)
    







