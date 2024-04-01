from django.db.models.signals import post_save, post_delete 
from django.dispatch import receiver 
from .models import CourseProgress, PageCompletion 
from .models import Page 


@receiver(post_delete,sender=Page) 
def calculate_course_progress_percentage(sender, instance, **kwargs):
   
       course = instance.module.course 
       no_completed_pages_of_course = 0
       no_pages = 0 
       cp_courses = CourseProgress.objects.filter(course=course) 
       print("progresses .....")
       print(cp_courses) 
       
       for progressObj in cp_courses:
             course = progressObj.course 
             student = progressObj.student 
            
             for module in course.modules.all():
               no_pages += module.pages.all().count() 

             try:
                completed_page = PageCompletion.objects.filter(student=student) 

             except PageCompletion.DoesNotExist:
               completed_page  = None 

             if completed_page is not None:   
                for module in course.modules.all():
                        for page  in module.pages.all():
                            for pc in completed_page:
                                if pc.page.id == page.id:
                                    print(pc.page)
                                    print(page)
                                    print("-------------------")

                                    no_completed_pages_of_course += 1

             percentage = (((no_completed_pages_of_course)/no_pages) * 100)

             progressObj.progress = percentage 
             progressObj.save() 

@receiver(post_save,sender=Page)
def calculate_course_progress_percentage(sender, instance, created,**kwargs):
    if created:
       print("created hacker") 
    #    print(dir(sender.page.module))  
       
       course = instance.module.course 
       no_completed_pages_of_course = 0
       no_pages = 0 
       cp_courses = CourseProgress.objects.filter(course=course) 
       print("progresses .....")
       print(cp_courses) 
       
       for progressObj in cp_courses:
             course = progressObj.course 
             student = progressObj.student 
            
             for module in course.modules.all():
               no_pages += module.pages.all().count() 

             try:
                completed_page = PageCompletion.objects.filter(student=student) 

             except PageCompletion.DoesNotExist:
               completed_page  = None 

             if completed_page is not None:   
                for module in course.modules.all():
                        for page  in module.pages.all():
                            for pc in completed_page:
                                if pc.page.id == page.id:
                                    print(pc.page)
                                    print(page)
                                    print("-------------------")

                                    no_completed_pages_of_course += 1

             percentage = (((no_completed_pages_of_course)/no_pages) * 100)

             progressObj.progress = percentage 
             progressObj.save() 

@receiver(post_delete, sender=PageCompletion)
def calculate_course_progress_percentage(sender, instance, **kwargs):
   
       student = instance.student 
       course = instance.page.module.course
       no_completed_pages_of_course = 0
       no_pages = 0 

       for module in course.modules.all():
           no_pages += module.pages.all().count() 

       try:
            completed_page = PageCompletion.objects.filter(student=student) 

       except PageCompletion.DoesNotExist:
           completed_page  = None 

       if completed_page is not None:   
            for module in course.modules.all():
                    for page  in module.pages.all():
                        for pc in completed_page:
                            if pc.page.id == page.id:
                                print(pc.page)
                                print(page)
                                print("-------------------")

                                no_completed_pages_of_course += 1

       percentage = (((no_completed_pages_of_course)/no_pages) * 100)

       cp = CourseProgress.objects.get(course=course,student=student) 
       cp.progress = percentage 
       cp.save()
       
@receiver(post_save, sender=PageCompletion) 
def calculate_course_progress_percentage(sender, instance, created,**kwargs):
    if created:
       print("created hacker") 
    #    print(dir(sender.page.module))  
       
       student = instance.student 
       course = instance.page.module.course
       no_completed_pages_of_course = 0
       no_pages = 0 

       for module in course.modules.all():
           no_pages += module.pages.all().count() 

       try:
            completed_page = PageCompletion.objects.filter(student=student) 

       except PageCompletion.DoesNotExist:
           completed_page  = None 

       if completed_page is not None:   
            for module in course.modules.all():
                    for page  in module.pages.all():
                        for pc in completed_page:
                            if pc.page.id == page.id:
                                print(pc.page)
                                print(page)
                                print("-------------------")

                                no_completed_pages_of_course += 1

       percentage = (((no_completed_pages_of_course)/no_pages) * 100)

       try:
           
            cp = CourseProgress.objects.get(course=course,student=student)  
            cp.progress = percentage 
            cp.save()

       except CourseProgress.DoesNotExist:
            print("Errorr is here!!")
            CourseProgress(student=student, course=course,progress=percentage).save()
            print("something!!!!!!!!!!!!")

       print(" show me something!!!!!!!!!!!!")
