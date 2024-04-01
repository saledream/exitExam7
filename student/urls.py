from django.urls import path, include, re_path 
from . import views 

urlpatterns =[

    path("", views.dashboard, name="student_dashboard"),
    path("fetch/all/", views.fetch, name="fetch"),
    path("fetch/courses/<str:status>/", views.courses, name="courses"),
    path("fetch/course/<int:pk>/", views.get_course, name="course"), 
    path("fetch/modules/<int:pk>/<int:course_id>/", views.get_module, name="module"),
    path("fetch/pages/<int:pk>/", views.get_page, name="page"),
    path("pageCompletion/<int:pk>/<str:complete>/", views.page_complete, name="page_complete"),
    path("alpine/", views.alpine, name="alpine"),   
    path("fetch/models/", views.get_models_all,name="all_models"), 
    path("fetch/models/<int:id>/", views.get_models, name="models"), 
    path("fetch/models/<str:view>/", views.get_model_view, name="model_view"),
    path("fetch/tests/", views.get_tests,name="tests"),
    path("fetch/tests/<slug:slug>/",views.course_tests, name="course_tests"), 
    path("take/exam/test/<int:test_id>/", views.take_test_exam, name="take_test"), 
    path("take/exam/test/answer/<int:test_id>/<int:q_id>/<slug:slug>/", views.exam_test_answer, name="test_answer"), 
    path("take/exam/test/next_question/<int:test_id>/<int:q_id>/", views.exam_test_next_question, name="next_test_question"), 
    path("take/exam/model/<int:model_id>/", views.take_model_exam, name="take_model"), 
    path("take/exam/model/answer/<int:model_id>/<int:q_id>/<slug:slug>/", views.exam_model_answer, name="model_answer"), 
    path("take/exam/model/next_question/<int:model_id>/<int:q_id>/", views.exam_model_next_question, name="next_model_question"), 
    path("models/", views.models, name="models"),
    path("modules/", views.modules, name="modules"),
    path("pages/",views.pages, name="pages"),
    path("cppages/", views.cppages, name="cp_pages"),
    path("questions/", views.questions, name="questions"), 
    path("tests/",views.tests, name="test"), 

]