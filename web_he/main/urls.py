from django.urls import path, include
from . import views

urlpatterns = [
    path('intro/', views.intro),
    path('login/', views.login),
    path('project/', views.ProjectList.as_view()),
    path('project/<int:pk>/', views.ProjectDetail.as_view()),
    path('img/', views.img),
    ]