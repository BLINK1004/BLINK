from django.contrib import admin
from .models import MImgProject, ProjectForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Register your models here.

admin.site.register(MImgProject)
admin.site.register(ProjectForm)
# admin.site.register(Muser)

class ProfileInline(admin.StackedInline): # 로또 프로젝트에서 썼던 방식으로 유저 밑에 프로필 을 붙여서 보여주려고 이를 상속받음
    model = Profile
    con_delete = False                    # 프로필을 아예 없앨 수 없게 하는 속성(한번 만들면 지우는건 이상하니까)

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

# 기존의 User의 등록을 취소했다가 User와 ProfileInline을 붙임.
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)