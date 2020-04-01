from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Project
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.contrib import auth

class ProjectList(ListView):
    model = Project

    def get_queryset(self):
        return Project.objects.order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectList, self).get_context_data(**kwargs)

        return context

class ProjectDetail(DetailView):
    model = Project

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        return context

def intro(request):
    projects = Project.objects.all()

    return render(
        request,
        'main/intro.html',
        {
            'projects': projects,
        }
    )

def login(request):
    return render(
        request,
        'main/login.html',
    )

def logout(request):
        auth.logout(request)
        return redirect('intro')

def img(request):
    return render(
        request,
        'main/img.html',
    )