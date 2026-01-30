from django.urls import path
from RecruitersApp import views
urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('AdminAction', views.adminaction),
    path('AdminHome', views.AdminHome),
    path('AddDept', views.AddDept),
    path('AddDeptAction', views.AddDeptAction),
    path('ViewDept', views.ViewDept),
    path('delete', views.delete),
    path('PostApplicaiton', views.PostApplication),
    path('AddTAVacancyAction', views.AddTAVacancyAction),
    path('ViewApplicaiton', views.ViewApplicaiton),
    path('AcceptVacancy', views.AcceptVacancy),
    path('DeclineVacancy', views.DeclineVacancy),
    path('ViewAllTA', views.ViewAllTA),
    path('ViewResume', views.ViewResume),

]
