from django.shortcuts import render, redirect
from django.urls import reverse
from .models import MImgProject
from .forms import PostForm
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from . import cv_function
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404


class ProjectList(ListView):
    model = MImgProject

    def get_queryset(self):
        return MImgProject.objects.order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectList, self).get_context_data(**kwargs)
        return context

class ProjectDetail(LoginRequiredMixin,FormMixin, DetailView):
    model = MImgProject
    form_class = PostForm

    def get_success_url(self):
        print(ConnectionRefusedError)
        return reverse('main:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        context['form'] = PostForm(initial={
            'text': '',
        })
        context['mimgproject'].img_temp = context['mimgproject'].img_origin
        context['mimgproject'].save()
        context['user'] = self.request.user
        imageURL = context['mimgproject'].img_temp.name
        path = settings.MEDIA_ROOT + '/' + imageURL
        print(path)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        # print("form")
        # print(form)
        # print("===========================")
        # new_form = form.cleaned_data['text']
        # print("new_form")
        # print(new_form)
        # print("===========================")

        if form.is_valid():
            print("Valid")
            return self.form_valid(form)
        else:
            print("inValid")
            return self.form_invalid(form)

    def form_valid(self, form):
        print("form")
        print(form)
        print("===========================")
        print("In form_valid")
        projectform = form.save(commit=False)
        print("check1")
        print("check!111")
        projectform.project = get_object_or_404(MImgProject, pk=self.object.pk)
        print("check2")
        projectform.writer = self.request.user
        print("check3")
        projectform.save()
        print("check4")
        return super(ProjectDetail, self).form_valid(form)

       # print(type(context['mimgproject'].img_origin))
        #
        # if self.request.method == 'GET':
        #     context['form'] = GetForm(self.request.POST)
        #
        #     # db에 이미지 update 정상적으로 되는지 확인
        #     context['mimgproject'].img_temp = context['mimgproject'].img_origin
        #     context['mimgproject'].save()
        #
        #     imageURL = context['mimgproject'].img_temp.name
        #     path = settings.MEDIA_ROOT + '/' + imageURL
        #     print(path)
        #
        #     # opencv 함수 실행 확인
        #     cv_function.im_read(path)



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


