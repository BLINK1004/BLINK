from django import forms
from .models import ProjectForm

class PostForm(forms.ModelForm):
    # Form을 통해 사용자가 입력한 box의 데이터를 받아온다
    class Meta:
        model = ProjectForm
        fields = ['text']