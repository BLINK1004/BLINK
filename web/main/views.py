from django.shortcuts import render
from .models import Project
from django.views.generic import ListView

class ProjectList(ListView):
    model = Project

    def get_queryset(self):
        return Project.objects.order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectList, self).get_context_data(**kwargs)

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

