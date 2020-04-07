from django.shortcuts import render, redirect
from django.urls import reverse
from .models import MImgProject
from .forms import GetForm
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from . import cv_function


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
        print(type(context['mimgproject'].img_origin))

        if self.request.method == 'GET':
            context['form'] = GetForm(self.request.POST)

            # db에 이미지 update 정상적으로 되는지 확인
            context['mimgproject'].img_temp = context['mimgproject'].img_origin
            context['mimgproject'].save()

            imageURL = context['mimgproject'].img_temp.name
            path = settings.MEDIA_ROOT + '/' + imageURL
            print(path)

            # opencv 함수 실행 확인
            cv_function.im_read(path)

        return context

class ProjectCreate(LoginRequiredMixin, CreateView):
    model = MImgProject
    fields = ('title','img_origin','description')
    # fields = '__all__'

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user

            mimgproject = form.save(commit=False)
            mimgproject.description = 'hihihi'
            # user 필드에 현재 로그인되어 있는 유저를 저장
            mimgproject.user = self.request.user

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


