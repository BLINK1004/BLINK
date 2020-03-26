from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Photo(models.Model):
    title = models.TextField(default='')
    file = models.ImageField(upload_to='main/%y/%m/%d/')
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return '{}'.format(self.title)

    def get_absolute_url(self):
        return '/main/{}/'.format(self.pk)

    def get_update_url(self):
        return self.get_absolute_url() + 'update/'

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'
