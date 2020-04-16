from django.shortcuts import render, redirect
from django.urls import reverse
from .models import MImgProject, ProjectForm
from .forms import PostForm, UserForm, ProfileForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from . import cv_function
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from django.views import View
from django.http import HttpResponse


class ProjectList(ListView):
    model = MImgProject

    def get_queryset(self):
        return MImgProject.objects.order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectList, self).get_context_data(**kwargs)
        return context

def post(request, pk):
    post = get_object_or_404(MImgProject, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            print(form)
            return redirect('detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        print(form)
        context = {
            'form':form,
            'post':post,
        }
        return render(request, 'main/detail.html', context)

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

class ProfileView(DetailView):
    context_object_name = 'profile_user' # model로 지정해준 User모델에 대한 객체와 로그인한 사용자랑 명칭이 겹쳐버리기 때문에 이를 지정해줌.
    model = User
    template_name = 'main/profile.html'

class ProfileUpdateView(View): # 간단한 View클래스를 상속 받았으므로 get함수와 post함수를 각각 만들어줘야한다.
    # 프로필 편집에서 보여주기위한 get 메소드
    def get(self, request):
        user = get_object_or_404(User, pk=request.user.pk)  # 로그인중인 사용자 객체를 얻어옴
        user_form = UserForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
        })

        if hasattr(user, 'profile'):  # user가 profile을 가지고 있으면 True, 없으면 False (회원가입을 한다고 profile을 가지고 있진 않으므로)
            profile = user.profile
            profile_form = ProfileForm(initial={
                'user': profile.user,
                'nickname': profile.nickname,
                'profile_photo': profile.profile_photo,
                'birth_date': profile.birth_date,
            })
        else:
            profile_form = ProfileForm()

        return render(request, 'main/profile_update.html', {"user_form": user_form, "profile_form": profile_form})

    def post(self, request):
        u = User.objects.get(id=request.user.pk)  # 로그인중인 사용자 객체를 얻어옴
        user_form = UserForm(request.POST, instance=u)  # 기존의 것의 업데이트하는 것 이므로 기존의 인스턴스를 넘겨줘야한다. 기존의 것을 가져와 수정하는 것

        # User 폼
        if user_form.is_valid():
            user_form.save()

        if hasattr(u, 'profile'):
            profile = u.profile
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)  # 기존의 것 가져와 수정하는 것
        else:
            profile_form = ProfileForm(request.POST, request.FILES)  # 새로 만드는 것

        # Profile 폼
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)  # 기존의 것을 가져와 수정하는 경우가 아닌 새로 만든 경우 user를 지정해줘야 하므로
            profile.user = u
            profile.save()

        return redirect('profile', pk=request.user.pk)  # 수정된 화면 보여주기

def img(request):
    return render(
        request,
        'main/img.html',
    )


