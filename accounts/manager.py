from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):

    def _create_user(self, email,username,password):
        if not email:
              raise ValueError("The email must be provided") 
        email = self.normalize_email(email) 
        user = self.model(email=email,username=username) 
        user.set_password(password) 
        user.save(using=self._db) 
        return user 
         
    def create_user(self,email, username,password=None):
        return self._create_user(email, username,password)  
    
    def create_student(self, email,username,password=None):
         user = self.create_user(email,username,password) 
         user.user_type = 'student'  
         user.save(using=self.db) 
         return user 

    def create_instructor(self, email, username,password=None):
         user = self.create_user(email,username,password) 
         user.user_type = 'instructor'
         user.is_staff = True  
         user.save(using=self.db)
         return user  
    
    def create_admin(self, email,username, password=None):
         user = self.create_user(email,username,password) 
         user.user_type = 'admin'
         user.is_staff = True  
         user.save(using=self.db) 
         return user 
    
    def create_superuser(self,email,username,password=None) : 
         
        user = self.create_user(email,username,password)
        user.is_superuser = True 
        user.is_staff = True 

        user.save(using=self.db)
        return user  

