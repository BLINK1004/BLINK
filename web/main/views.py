from .models import MImgProject
from .forms import PostForm, UserForm, ProfileForm

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

import json
import cv2
from . import cv_function

from querystring_parser import parser

import uuid

class ProjectList(ListView):
    model = MImgProject

    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_authenticated:
            return MImgProject.objects.order_by('-created')
        else:
            return redirect('intro')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectList, self).get_context_data(**kwargs)
        return context

def edit(request, pk):
    post = get_object_or_404(MImgProject, pk=pk)
    if request.method == "POST" and request.is_ajax:
        print("request POST AJAX")
        print(request.POST)
        post_dict = parser.parse(request.POST.urlencode())

        if 'input_box' in post_dict.keys():
            print('확인.')
            print(post_dict)
            print("==========post_dict++++++++++++")
            print(post_dict["input_box"])
            post.input_box = post_dict["input_box"]
            post.save()

        elif 'txt' in post_dict.keys():
            font_path = "./main/ML/IndieFlower-Regular.ttf"

            size = (64, 64)
            sentense = post_dict['txt']

            if len(sentense) > 10 :
                print('10글자 이상 제한')
                return redirect('edit', pk=post.pk)

            for char in sentense:
                save_path = settings.MEDIA_ROOT + '/' + post.img_view.name[:-4] + "_" + str(post.pk) + str(char) + ".png"
                print(save_path)
                cv_function.gen_char(font_path, size, char, save_path)

            print('txt확인')
            print(post_dict)

        return redirect('edit', pk=post.pk)

    else:
        return render(request, 'main/edit.html', {"post":post})

    # return render(request, 'main/edit.html', {"post":post})

def post(request, pk):
    post = get_object_or_404(MImgProject, pk=pk)

    if request.method == "POST":
        # record
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            # 사용자 입력 box
            dic = json.loads(request.POST['input_history'])

            boxs = []
            for d in dic['path']:
                boxs.append([int(d['x']), int(d['y']), int(d['width']), int(d['height'])])
            print(boxs)

            # 원본 이미지 경로
            # origin_URL = settings.MEDIA_ROOT + '/' + post.img_origin.name
            # 마스크 이미지 경로
            mask_URL = settings.MEDIA_ROOT + '/' + post.img_mask.name
            # inpaint 이미지 경로
            inpaint_URL = settings.MEDIA_ROOT + '/' + post.img_inpaint.name
            # view 이미지 경로
            view_URL = settings.MEDIA_ROOT + '/' + post.img_view.name
            # ocr data
            ocr_data = post.ocr_data

            # user box 토대로 change image 저장
            img = cv_function.pixel_change(view_URL, inpaint_URL, boxs)
            # over write
            cv2.imwrite(view_URL, img)

            # pixel_change
            # record : x ,y ,width ,height, center, txt, style
            lst = []
            for b in boxs:
                record = dict()
                record['x'] = b[0]
                record['y'] = b[1]
                record['w'] = b[2]
                record['h'] = b[3]

                box = [record['x'], record['y'], record['w'], record['h']]
                record['center'] = cv_function.init_center(mask_URL, box)
                try:
                    # 현재 박스안에 ocr의 텍스트가 있을경우 추출
                    record['txt'] = cv_function.spell_check(cv_function.find_txt(box, ocr_data))
                    print(record['txt'], type(record['txt']))

                    # 맞춤법검사 및 번역 api
                    record['t_txt'] = cv_function.trans_papago(record['txt'])
                    print(record['t_txt'], type(record['t_txt']))

                except:
                    # 현재 박스안에 ocr의 텍스트가 없을경우
                    print('텍스트 검출 실패')
                    record['txt'] = ''
                    record['t_txt'] = ''

                record['style'] = ''
                record['font'] = 'Metal Mania'
                record['fontSize'] = '14px'
                record['pk'] = str(uuid.uuid4())[0:6]

                print(" 레코드 확인 ! ")

                print(record)
                lst.append(record)
            try:
                # record가 있을 경우
                box_lst = json.loads(post.input_box)
            except:
                # record가 없을 경우
                box_lst = []

            # 기존 박스데이터에 현재 입력한 박스 추가
            for r in lst:
                box_lst.append(r)

            post.input_box = json.dumps(box_lst)

            # 데이터 베이스 저장
            form = PostForm(request.POST, instance=post)
            post = form.save()

            return redirect('detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        context = {
            'form':form,
            'post':post,
        }
        return render(request, 'main/detail.html', context)

class ProjectCreate(LoginRequiredMixin, CreateView):
    model = MImgProject
    fields = ('title','img_view','description')
    # fields = '__all__'

    def form_valid(self, form):
        current_user = self.request.user

        if current_user.is_authenticated:
            form.instance.author = current_user

            mimgproject = form.save(commit=False)
            # user 필드에 현재 로그인되어 있는 유저를 저장
            mimgproject.user = self.request.user
            mimgproject.save()

            viewURL = settings.MEDIA_ROOT + '/' + mimgproject.img_view.name
            cv_function.init_resize(viewURL)
            ocr_data = cv_function.detect_text(viewURL) # OCR google API 사용
            mimgproject.ocr_data = ocr_data

            # segmentation model run
            maskURL = mimgproject.img_view.name[:-4] + '_mask.jpg'
            print(maskURL)
            cv_function.predict_seg(viewURL, maskURL)
            # cv_function.predict_seg_unet(viewURL, maskURL)
            mimgproject.img_mask = maskURL
            mimgproject.save()

            # inpaint model run
            maskURL_ = settings.MEDIA_ROOT + '/' + mimgproject.img_mask.name
            inpURL = mimgproject.img_view.name[:-4] + '_inp.jpg'
            print(inpURL)
            # cv_function.predict_pconv_inp(viewURL, maskURL_, inpURL)
            cv_function.predict_inp_gan(viewURL, maskURL_, inpURL)

            mimgproject.img_inpaint = inpURL

            view_img = cv2.imread(viewURL)
            ori_img = view_img.copy()

            oriURL = mimgproject.img_view.name[:-4] + '_ori.jpg'
            print(settings.MEDIA_ROOT + '/' + oriURL)
            cv2.imwrite(settings.MEDIA_ROOT + '/' + oriURL, ori_img)

            mimgproject.img_origin = oriURL# original 이미지 백업
            mimgproject.save()

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
        user_form = UserForm(request.POST, instance=u)  # 기존의 것을 업데이트하는것 이므로 기존의 인스턴스를 넘겨줘야한다. 기존의 것을 가져와 수정하는 것

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