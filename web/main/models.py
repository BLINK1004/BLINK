from django.db import models

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    created = models.DateTimeField()

    def __str__(self):
        return '{}'.format(self.title)