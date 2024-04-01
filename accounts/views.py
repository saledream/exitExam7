from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect  
from .forms import SignUpForm, LoginForm  
from django.contrib.auth import authenticate, login ,logout
from django.urls import reverse  
from django.urls import reverse_lazy 
from django.contrib.auth.views import PasswordResetView, PasswordChangeDoneView, PasswordResetCompleteView,PasswordResetConfirmView  
from django.contrib.messages.views import SuccessMessageMixin 
from django.http import HttpResponse 
from django.contrib import messages 
from .models import User 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.views import LoginView 

def signup(request):
    
    if request.method == 'POST':

        form = SignUpForm(request.POST) 
        
        if form.is_valid():
            form.save() 
            messages.success(request,"registration is successful") 
            return redirect(reverse("account:login"))

        else:
            print(form.errors)
            
            for error in form.errors:
               messages.error(request,form.errors[error])
           
    form = SignUpForm()
    return render(request, 'accounts/signup.html',{'form':form})
 

def mylogin(request):

    if request.method == 'POST':
        form = LoginForm(request.POST) 
        print(form) 

        if form.is_valid():
            email = form.cleaned_data['email'] 
            password = form.cleaned_data['password'] 
            user = authenticate(request, email=email,password=password) 
            if user is not None:
                if user.user_type == 'student': 
                    login(request, user) 
                    return redirect(reverse('student_dashboard')) 

                elif user.user_type == "instructor":
                    login(request, user) 
                    return redirect("/admin/") 
                elif user.is_superuser or user.user_type == 'admin':
                    login(request,user) 
                    return redirect("/admin/") 
                
            else:        
                messages.error(request,"Invalid email or password") 

        else:
             for error in form.errors:
                    messages.error(request,form.errors[error]) 
    form = LoginForm() 
    
    return render(request, 'accounts/login.html',{'form':form})

@login_required
def mylogout(request):

    if request.user.user_type == 'instructor' or request.user.user_type == 'admin' or request.user.is_superuser:
       logout(request)
       return redirect("/accounts/logout/") 
    
    else:
         return redirect("/") 
    
    
@login_required
def dashboard(request):

    return render(request, 'registration/dashboard.html', {'section':'dashboard'})

def profileEdit(request):
    pass 



def viewProfile(request):
    pass 



def check_username(request):
      username = request.POST.get('username') 
     
      if User.objects.filter(username=username).exists():
            return HttpResponse("<div id='username-error' class='error'> This username already exists </div>") 
      
      else:
           return HttpResponse("<div id='username-error' class='success'> This username is available </div>")
      
import re 
def check_password(request):
      
      progress_bar = '''
                        <div class="progress">
                           <div class="progress-bar" role="progressbar" aria-valuenow="%d" aria-valuemin="0" aria-valuemax="100">%s</div>
                       </div> 
                    '''

      digit = r'[0-9]+'
      upper = r'[A-Z]+'
      lower = r'[a-z]+' 

      password = request.POST.get('password1')

     
      if (re.search(digit, password) and re.search(upper,password) and re.search(lower,password) and len(password) > 8) or (len(password) > 10):
          return HttpResponse(progress_bar%(100,'Strong password'))  
      
      elif ((re.search(digit, password) or re.search(upper,password)) or (re.search(lower,password) or re.search(upper,password)) or (re.search(digit,password) or re.search(lower,password))) and len(password) > 8:
           return HttpResponse("<div> Medium </div>") 
      
      else:
           return HttpResponse("<div> Weak password</div>") 

def check_email(request):
      regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
      email = request.POST.get('email') 
       
      if  re.fullmatch(regex, email) :
            if User.objects.filter(email=email).exists():
                return HttpResponse("<div id='username-error' class='error'> This email already exists </div>") 
            
            else:
               return HttpResponse("<div id='username-error' class='success'> This email is available </div>")

      else:

        return HttpResponse("<div id='username-error' class='error'> Invalid email  </div>")


class ResetPasswordView(SuccessMessageMixin,PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('password_reset_done')




      
  