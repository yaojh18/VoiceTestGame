# Generated by Django 3.0.8 on 2020-10-13 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0002_auto_20201007_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='city',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='level',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='province',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
