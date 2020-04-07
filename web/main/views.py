from django.shortcuts import render, redirect
from django.urls import reverse
from .models import MImgProject
from .forms import PostForm, UserForm, ProfileForm
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from . import cv_function
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from django.views import View


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

    def get_success_url(self): #post 처리가 성공한 뒤 행할 행동
        print(ConnectionRefusedError)
        return reverse('main:detail', kwargs={'pk': self.object.pk}) #디테일뷰 다시 보여주기

    def get_context_data(self, **kwargs): #template에 보낼 context 설정
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        context['form'] = PostForm(initial={
            'text': '', #textfield에 default value 설정
        })
        context['mimgproject'].img_temp = context['mimgproject'].img_origin
        context['mimgproject'].save()
        context['user'] = self.request.user #user 이름 표시

        imageURL = context['mimgproject'].img_temp.name
        path = settings.MEDIA_ROOT + '/' + imageURL
        print(path)

        return context

    def post(self, request, *args, **kwargs): #POST 요청이 들어왔을 때
        self.object = self.get_object() #현재 페이지 object get
        form = self.get_form() #form 데이터 받아오기

        if form.is_valid(): #form 내용이 정상적일 경우
            return self.form_valid(form) #form_valid 함수 콜
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        projectform = form.save(commit=False) #form 데이터를 저장, 그러나 쿼리 실행 X
        projectform.project = get_object_or_404(MImgProject, pk=self.object.pk)
        #MImgProject를 call
        projectform.writer = self.request.user #작성자 설정
        projectform.save() #수정된 내용 저장 후 쿼리 실행
        return super(ProjectDetail, self).form_valid(form)


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


