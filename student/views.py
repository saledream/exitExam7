from django.shortcuts import render, get_object_or_404 
from django.http import HttpResponse 
from accounts.models import User 
from EECommittee.models import Course, Department 
from instructor.models import Module, Page, Exam_Model, Test, PageCompletion, ModelQuestion, TestQuestion 
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse, JsonResponse  
from instructor.models import CourseProgress 
from django.template.defaultfilters import slugify 
from instructor.models import ExamResult, ExamStatus   
from django.contrib import messages 

# Create your views here.

@login_required
def dashboard(request):
    
        print(User.objects.all())
        modelsExams = Exam_Model.objects.filter(dept__name="computer science") 

        return render(request, 'student/index.html',{'users':User.objects.all(),"modelExam":modelsExams})

login_required
def fetch(request): 
      user = request.user 
      print(user.department) 
      courses = Course.objects.all().filter(dept=request.user.department)  
      modelExams = Exam_Model.objects.filter(dept=request.user.department)
      models = []
      for model in modelExams:
           hard = ModelQuestion.objects.filter(modeExam=model,question_type="hard").all().count() or 0
           medium = ModelQuestion.objects.filter(modeExam=model,question_type="medium").count()  or 0
           easy = ModelQuestion.objects.filter(modeExam=model,question_type="easy").count() or 0

           models.append([model,{
                 "hard":hard,
                "medium": medium,
                "easy":easy
           }])
          # models.append(model)
      tests = []
      for course in courses:
           c_tests = Test.objects.filter(course=course)
           for test in c_tests:
               hard = TestQuestion.objects.filter(testExam=test,question_type="hard").all().count() or 0
               medium = TestQuestion.objects.filter(testExam=test,question_type="medium").all().count() or 0
               easy = TestQuestion.objects.filter(testExam=test,question_type="easy").all().count() or 0 

               tests.append([test,course.name,{
                "hard":hard,
                "medium":medium,
                "easy":easy
               }])
           
          #  tests.append(c_tests)
      
      courses_progress= [] 
      for course in courses:
           try:
              
              cp = CourseProgress.objects.get(course=course)
              progress = cp.progress 

           except CourseProgress.DoesNotExist:
                progress = 0 
           courses_progress.append([course,progress]) 
           
      print("saleamlak")
      return render(request,"partials/all_dashboard.html",{'courses':courses_progress,"models": models,"tests":tests,"title":"all content"}) 
      
@login_required
def courses(request, status): 
      courses = Course.objects.all().filter(dept=request.user.department)  
      courses_progress= [] 

      if status == 'all':
          for course in courses:
               try:
               
                    cp = CourseProgress.objects.get(course=course)
                    progress = cp.progress 

               except CourseProgress.DoesNotExist:
                    progress = 0 
               courses_progress.append([course,progress]) 

      elif status == 'inprogress':
          
          for course in courses:
               try:
               
                    cp = CourseProgress.objects.get(course=course)
                    if cp.progress > 0:
                         courses_progress.append([course,cp.progress])

               except CourseProgress.DoesNotExist:
                   pass 
          
      else:
           pass 
           
      return render(request,"partials/courses.html",{'courses':courses_progress}) 
       

      
@login_required
def get_course(request,pk): 
      
      onclick_url = "fetch/course/{}/".format(pk) 
      nav_title = "modules" 
      modules = None 
      print(onclick_url) 
      try:
         course = Course.objects.get(id=pk)
         modules = course.modules.all() 
      except Course.DoesNotExist as e:
          pass 

      return render(request,"partials/modules.html",{'modules':modules,"url":onclick_url,"title":nav_title,"course_id":pk}) 
       
@login_required
def get_module(request,pk,course_id=None): 
      
      module = None 
      onclick_url = "fetch/modules/{}/".format(pk) 
      nav_title = ""
      try:
         module = get_object_or_404(Module,id=pk)
         nav_title = module.name 
      except Exception as e:
          print(" what is going on")

      return render(request,"partials/pages.html",{'module':module,"url":onclick_url,"title":nav_title,"course_id":course_id}) 

def get_page(request,pk): 
      
      page = None 
      completed = False 
      try:
         
         page = Page.objects.get(id=pk)
         completed = PageCompletion.objects.get(page=page) 
         completed = True 

      except Page.DoesNotExist:
          page = None 

      except PageCompletion.DoesNotExist:
           completed = False 

      return render(request,"partials/page.html",{'page':page,'completed':completed}) 

def alpine(request):
     
     return render(request,"partials/alpine.html",{"love":'you'})

def page_complete(request,pk,complete):
     
     print(pk,complete) 
     page = None 

     try:
           page = Page.objects.get(id=pk)  
           print(page, "oooooooooo", request.user) 
           if page is not None and complete.lower() == 'true':
                 
                 try:
                      page_complete = PageCompletion.objects.get(page=page)
                      print(page_complete)
                      print(page) 
                      print("-------------------")
                 except PageCompletion.DoesNotExist: 
                        marked = PageCompletion.objects.create(page=page, student=request.user) 
                        marked.save()
                        print("saved successs!!!!!") 

           elif page is not None and complete.lower() == 'false':
                unmark = PageCompletion.objects.filter(page=page)
                for page in unmark:
                     page.delete()  

                print("successs!! delete")

           return HttpResponse("marked")
     
     except Page.DoesNotExist:
         pass 
    
     return HttpResponse("unmarked")
                                           
import json 

def take_test_exam(request,test_id):  
        
        q = None
        next_id = None  
        finished = False 
        total_q = 0 
        try:
           test = Test.objects.get(id=test_id) 
           q = test.test.all()[0] 
           total_q = test.test.all().count() 
           next_id = 0

        except (Test.DoesNotExist,IndexError):
             q = None 
             next_id = 0 
         
        return render(request, "partials/take_test_exam.html",{'question':q,'next_id':next_id,"title":test.title,"total_q":total_q})

def course_tests(request, slug):
       
       tests = [] 
       try:
           if slug == "all_all":
               courses = Course.objects.all().filter(dept=request.user.department)
               for course in courses:
                    c_tests = Test.objects.filter(course=course)
                    for test in c_tests:
                         hard = TestQuestion.objects.filter(testExam=test,question_type="hard").all().count() or 0
                         medium = TestQuestion.objects.filter(testExam=test,question_type="medium").all().count() or 0
                         easy = TestQuestion.objects.filter(testExam=test,question_type="easy").all().count() or 0 

                         tests.append([test,course.name,{
                         "hard":hard,
                         "medium":medium,
                         "easy":easy
                         }])
           else:
               course = Course.objects.get(slug=slug)

               c_tests = Test.objects.filter(course=course)
               for test in c_tests:
                    hard = TestQuestion.objects.filter(testExam=test,question_type="hard").all().count() or 0
                    medium = TestQuestion.objects.filter(testExam=test,question_type="medium").all().count() or 0
                    easy = TestQuestion.objects.filter(testExam=test,question_type="easy").all().count() or 0 

                    tests.append([test,course.name,{
                    "hard":hard,
                    "medium":medium,
                    "easy":easy
                    }])
          

       except Course.DoesNotExist:
           return 
       print("==========================================")
       print(tests)
       return render(request,"partials/tests.html",{"tests":tests})

def exam_test_answer(request, test_id,q_id,slug):
        
        test = Test.objects.get(id=test_id)  
        try:
           q = test.test.all()[q_id]  

        except IndexError:
             q = None 
  
        try:
             
          examstatus = ExamStatus.objects.get(student=request.user,question=q)
          examstatus.response = slug
          examstatus.save() 

        except ExamStatus.DoesNotExist:
            examstatus = ExamStatus(student=request.user,question=q,response = slug)
            examstatus.save() 

        return JsonResponse({"save":True}) 

def exam_test_next_question(request, test_id,q_id):
     test = Test.objects.get(id=test_id)
     next_id = q_id + 1 
     q = None 
     finished = False  

     try:
          q = test.test.all()[next_id]

     except IndexError as e: 
          print(e)
          q = None 
          finished = True 
     
     return render(request, "partials/take_test_exam.html",{"question":q, "test_id":test_id,"next_id":next_id,"finished":finished}) 

def get_models(request,id):
     
     return render(request,"partials/model_questions.html")

def get_model_view(request,view):
     
     modelExams = Exam_Model.objects.filter(dept=request.user.department)
     if view == 'asblock':
          return render(request,"partials/exam_block_view.html",{'models':modelExams}) 
     
     elif view == 'aslist':
         
          return render(request,"partials/exam_list_view.html",{'models':modelExams}) 
     
     else:
          pass 

def get_models_all(request):
      modelExams = Exam_Model.objects.filter(dept=request.user.department) 
      models = []
      for model in modelExams:
           hard = ModelQuestion.objects.filter(modeExam=model,question_type="hard").all().count() or 0
           medium = ModelQuestion.objects.filter(modeExam=model,question_type="medium").count()  or 0
           easy = ModelQuestion.objects.filter(modeExam=model,question_type="easy").count() or 0

           models.append([model,{
                 "hard":hard,
                "medium": medium,
                "easy":easy
           }])
      return render(request,"partials/models.html",{"models":models})

def get_tests(request):
      
      courses = Course.objects.all().filter(dept=request.user.department)   
      tests = []
      for course in courses:
           c_tests = Test.objects.filter(course=course)
           if len(c_tests)> 0:     
               for test in c_tests:
                    hard = TestQuestion.objects.filter(testExam=test,question_type="hard").all().count() or 0
                    medium = TestQuestion.objects.filter(testExam=test,question_type="medium").all().count() or 0
                    easy = TestQuestion.objects.filter(testExam=test,question_type="easy").all().count() or 0 

                    tests.append([test,course.name,{
                    "hard":hard,
                    "medium":medium,
                    "easy":easy
                    }])
      print(tests) 
      return render(request,"partials/all_tests.html",{"tests":tests,'courses':courses})  

def take_model_exam(request,model_id):
     
     models = Exam_Model.objects.filter(dept=request.user.department)
     model = models.get(id=model_id) 
     qs = model.question.all()
     total_q = model.question.all().count() 
     try:
          q, next_id = qs[0],0 

     except IndexError:
          q = None
          next_id = None   
     return render(request,"partials/take_model_exam.html",{'question':q,"total_q":total_q,'next_id':next_id,"model_id":model_id,"model_name":model.title}) 
  
def exam_model_answer(request,model_id,q_id,slug):
        
        models = Exam_Model.objects.filter(dept=request.user.department) 
        
        model = models.get(id=model_id) 
        try:
           q = model.question.all()[q_id]  
           messages.success(request,"submitted successfully")
        except IndexError:
             q = None 
      

     #    if  slugify(q.answer)  == slug:
             
     #         try:
              
     #           result = ExamResult.objects.get(exam=model,student=request.user)
     #           result.score += 1 
     #           result.save() 

     #         except ExamResult.DoesNotExist:
     #              result = ExamResult.objects.create(exam=model,student=request.user,exam_type="model",score=1) 
     #              result.save() 
        try:
             
          examstatus = ExamStatus.objects.get(student=request.user,question=q)
          examstatus.response = slug
          examstatus.save() 

        except ExamStatus.DoesNotExist:
            examstatus = ExamStatus(student=request.user,question=q,response = slug)
            examstatus.save() 
        print("show something!!!!!!!!")
        return JsonResponse({"save":True}) 

def exam_model_next_question(request, model_id,q_id):
    
     models = Exam_Model.objects.filter(dept=request.user.department)
     model = models.get(id=model_id)
     next_id = q_id + 1 
     q = None 
     finished = False  
     total_q = model.question.all().count() 
     try:
          q = model.question.all()[next_id]
         
     except IndexError as e: 
          print(e)
          q = None 
          finished = True 

     return render(request, "partials/take_model_exam.html",{"question":q, "model_id":model_id,"next_id":next_id,"finished":finished,"total_q":total_q,"model_name":model.title}) 

def models(request):
     all_model_exams = Exam_Model.objects.all()

     if request.user.is_authenticated:
         user_model_exams = all_model_exams.filter(dept=request.user.department).count()
         return render(request,"partials/static_data.html",{"data":user_model_exams})
  
     return render(request,"partials/static_data.html",{"data":user_model_exams.count()}) 

def modules(request):

     all_module = Module.objects.all()

     if request.user.is_authenticated:
          user_module = all_module.filter(instructor__username=request.user.username).count() 
          return render(request,"partials/static_data.html",{"data":user_module})
          return user_module 
     
     return render(request,"partials/static_data.html",{"data":user_module.count()})
     

def pages(request):
     all_pages = Page.objects.all()

     if request.user.is_authenticated:
          user_pages = all_pages.filter(instructor__username=request.user.username).count() 
          return render(request,"partials/static_data.html",{"data":user_pages}) 
     
     return render(request,"partials/static_data.html",{"data":user_pages.count()})
     

def cppages(request):
     
     cp_pages = PageCompletion.objects.all() 

     if request.user.is_authenticated:
          user_pages = Page.objects.filter(instructor__username=request.user.username) 
          user_page_completed = 0 
          for page in user_pages:
               for cp_page in cp_pages:
                    if page == cp_page:
                         user_page_completed += 1

          return render(request,"partials/static_data.html",{"data":user_page_completed})
     
     return render(request,"partials/static_data.html",{"data":cp_pages.count()}) 

def questions(request):
    
     q_total = ModelQuestion.objects.all().count() + TestQuestion.objects.all().count()

     if request.user.is_authenticated:
          user_modelQ = ModelQuestion.objects.filter(instructor__username=request.user.username)
          user_testQ = TestQuestion.objects.filter(instructor__username=request.user.username)
          q_total = user_modelQ.count() + user_testQ.count()  
          return render(request,"partials/static_data.html",{"data":q_total}) 
          

     return render(request,"partials/static_data.html",{"data":q_total}) 


def tests(request):

     tests = Test.objects.all()

     if request.user.is_authenticated:
           user_test = tests.filter(instructor__username=request.user.username).count() 

           return render(request,"partials/static_data.html",{"data":user_test})
     
     return render(request,"partials/static_data.html",{"data":user_test.count()})

