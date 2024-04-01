from django.urls import path, include 
from . import views 

urlpatterns =[

    path("", views.adminDashboard , name="admin-dashboard"),
]