# Generated by Django 2.2 on 2020-03-26 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(upload_to='main/%y/%m/%d/'),
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
