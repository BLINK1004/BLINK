from django.urls import path, include
from . import views

urlpatterns = [
    path('intro/', views.intro),
    path('login/', views.login),
    path('home/', views.ProjectList.as_view()),
]