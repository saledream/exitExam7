from django.contrib import admin
from .models import Department, Course 
# from django.contrib.auth.admin impor
# Register your models here.
from accounts.models import User 

class DepartmentModelAdmin(admin.ModelAdmin):
     list_display = ('name','No_courses','No_model_exams','instructors','students')  
     model = Course 
     search_fields = ('name',)
     # readonly_fields = ('instructor','dept') 
     def get_queryset(self, request) :
          
          qs = super().get_queryset(request) 
          if request.user.is_superuser or request.user.user_type == 'admin':
               return qs
          return  qs.filter(name=request.user.department)
 
admin.site.register(Department,DepartmentModelAdmin) 


class CourseModelAdmin(admin.ModelAdmin):
     list_display = ('name','instructor','department','No_modules','No_tests') 
     model = Course 
     list_filter = ('instructor','dept')
     search_fields = ('instructor__username','name','dept__name')
     exclude = ['slug',]
     def get_queryset(self, request) :
          
          qs = super().get_queryset(request) 
          if request.user.is_superuser or request.user.user_type == 'admin':
               return qs
          return  qs.filter(instructor=request.user)
        
admin.site.register(Course, CourseModelAdmin) 
