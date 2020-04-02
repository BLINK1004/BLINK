from django.db import models
'''
상대 모델에 접근하기
# N -> 1
MImgProject.user
MImgProject.user.user_id
MImgProject.user.user_name
'''
# Create your models here.
class Muser(models.Model):
    user_id = models.CharField(max_length=30)
    user_name = models.CharField(max_length=30)

    def __str__(self):
        return self.user_name


class MImgProject(models.Model):
    # 길이 제한이 있는 필드
    title = models.CharField(max_length=30)
    # 길이 제한이 없는 필드
    ocr_data= models.TextField(blank=True)
    img_origin = models.ImageField(upload_to='main/%y/%m/%d/', blank=True)
    img_mask = models.ImageField(upload_to='main/%y/%m/%d/', blank=True)
    img_inpaint = models.ImageField(upload_to='main/%y/%m/%d/', blank=True)
    description = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    # 유저하나에 프로젝트가 여러개
    user = models.ForeignKey(Muser, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.title)

    def get_absolute_url(self):
        return '/project/{}/'.format(self.pk)



