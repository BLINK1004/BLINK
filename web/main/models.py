from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

'''
상대 모델에 접근하기
# N -> 1
MImgProject.user
MImgProject.user.user_id
MImgProject.user.user_name
'''
# # Create your models here.
# class Muser(models.Model):
#     user_id = models.CharField(max_length=30)
#     user_name = models.CharField(max_length=30)
#
#     def __str__(self):
#         return self.user_name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # 현 계정의 사용자를 가져올 수 있음.
    nickname = models.CharField(max_length=64)
    profile_photo = models.ImageField(blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        return '/profile/{}/'.format(self.pk)


class MImgProject(models.Model):
    # 프로젝트 이름 필드 / 길이 제한이 있음
    title = models.CharField(max_length=30)

    # origin img를 ocr 모델에 넣은 값이 저장될 필드 / 길이 제한이 없는 필드
    ocr_data= models.TextField(blank=True)
    # 사용자에게 보여줄 이미지 필드
    img_view = models.ImageField(upload_to='main/%y/%m/%d/', blank=True)
    # history 데이터로 view 이미지를 생성해줄때 참조하는 기본 이미지 필드
    img_origin = models.ImageField(upload_to='main/%y/%m/%d/', blank=True)
    # segmentation model의 output을 저장할 필드
    img_mask = models.ImageField(upload_to='main/%y/%m/%d/', blank=True)
    # inpaint model의 output을 저장할 필드
    img_inpaint = models.ImageField(upload_to='main/%y/%m/%d/', blank=True)
    # 사용자가 입력한 box(x,y,w,h) 데이터 필드
    input_history = models.TextField(blank=True)

    # 사용자가 입력한 설명 필드
    description = models.CharField(max_length=50)
    # 만들어진 시각 필드
    created = models.DateTimeField(auto_now_add=True)

    # 프로젝트의 소유자 필드 (외래키) / 유저하나에 프로젝트가 여러개
    # https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#substituting-a-custom-user-model
    # https://wayhome25.github.io/django/2017/05/18/django-auth/
    User = get_user_model()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.title)

    def get_absolute_url(self):
        return '/project/{}/'.format(self.pk)


class ProjectForm(models.Model):
    User = get_user_model()
    project = models.ForeignKey(MImgProject, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return '{}'.format(self.writer)


