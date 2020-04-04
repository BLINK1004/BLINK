from django import forms
from .models import MImgProject

class GetForm(forms.ModelForm):
    # Form을 통해 사용자가 입력한 box의 데이터를 받아온다
    class Meta:
        model = MImgProject
        fields = ('input_history',)