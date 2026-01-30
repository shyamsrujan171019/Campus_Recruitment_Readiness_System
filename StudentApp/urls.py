from django.urls import path
from StudentApp import views


urlpatterns = [
    path('login', views.Login),
    path('Signup', views.Signup),
    path('RegAction', views.RegAction),
    path('LogAction', views.LogAction),
    path('ViewVacancies', views.ViewVacancies),
    path('ApplyJob', views.ApplyJob),
    path('ApplyAction', views.ApplyAction),
    path('App_Status', views.App_Status),
    path('SolveAssignment', views.SolveAssignment),
    path('UpdateSolution', views.UpdateSolution),
    path('VSolvedAssignment',views.VSolvedAssignment),
    path('ViewResume',views.ViewResume),
]
