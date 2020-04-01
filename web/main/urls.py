from django.urls import path, include
from . import views

urlpatterns = [
    path('intro/', views.intro, name='intro'),
    path('login/', views.login),
    path('logout/', views.logout),
    path('project/', views.ProjectList.as_view()),
    path('project/<int:pk>/', views.ProjectDetail.as_view()),
    path('img/', views.img),
    ]