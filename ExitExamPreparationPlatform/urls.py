
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include 

admin.site.site_header = "Exit Exam Preparation Platform "
admin.site.site_title = "Exit Exam Preparation platform"
admin.site.index_title = "Exit Exam Preparation Platform  Admin"
from accounts.views import mylogin 

urlpatterns = [
  path("", include("home.urls")),
  path("accounts/", include(("accounts.urls",'account'),namespace='account')),
  path("accounts/", include("django.contrib.auth.urls")), 
  path('students/',include("student.urls")),
  path('instructors/',include('instructor.urls')),
  path("admin/login/", mylogin, name="login"), 
  path('admin/', admin.site.urls),
  path('ckeditor/',include('ckeditor_uploader.urls')),
  path('imagefit/', include('imagefit.urls')),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)