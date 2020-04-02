from django.shortcuts import render, redirect
from django.urls import reverse
from .models import MImgProject
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin

class ProjectList(ListView):
    model = MImgProject

    def get_queryset(self):
        return MImgProject.objects.order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectList, self).get_context_data(**kwargs)

        return context

class ProjectDetail(DetailView):
    model = MImgProject

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        return context

class ProjectCreate(LoginRequiredMixin, CreateView):
    model = MImgProject
    fields = '__all__'

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(type(self), self).form_valid(form)
        else:
            return redirect('intro')


def intro(request):
    projects = MImgProject.objects.all()

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