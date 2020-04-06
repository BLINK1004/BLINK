from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('intro/', views.intro, name='intro'),
    path('login/', views.login),
    path('logout/', views.logout),
    path('project/', views.ProjectList.as_view()),
    path('project/<int:pk>/', views.ProjectDetail.as_view(),  name='detail'),
    path('create/', views.ProjectCreate.as_view()),
    path('img/', views.img),
    ]