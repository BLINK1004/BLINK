from django.urls import path, include
from . import views

urlpatterns = [
    path('intro/', views.intro, name='intro'),
    path('login/', views.login),
    path('logout/', views.logout),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile_update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('project/', views.ProjectList.as_view()),
    path('project/<int:pk>/', views.post, name='detail'),
    path('project/<int:pk>/edit', views.edit, name='edit'),
    path('create/', views.ProjectCreate.as_view()),
    path('img/', views.img),
    ]