from django import forms
from .models import ProjectForm, Profile
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    # Form을 통해 사용자가 입력한 box의 데이터를 받아온다
    class Meta:
        model = ProjectForm
        fields = ['text']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class ProfileForm(forms.ModelForm):
    profile_photo = forms.ImageField(required=False)
    class Meta:
        model = Profile
        fields = ['user', 'nickname', 'profile_photo', 'birth_date']