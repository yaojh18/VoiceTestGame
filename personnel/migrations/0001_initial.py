# Generated by Django 3.0.8 on 2020-11-12 14:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('media', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openid', models.CharField(max_length=128, unique=True)),
                ('gender', models.IntegerField(choices=[(0, 'Unknown'), (1, 'Male'), (2, 'Female')], null=True)),
                ('city', models.CharField(max_length=128, null=True)),
                ('province', models.CharField(max_length=128, null=True)),
                ('avatar_url', models.CharField(max_length=1024, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserAudio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio', models.FileField(max_length=512, upload_to='users/audio')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('score', models.FloatField(default=0.0)),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='media.OriginMedia')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audios', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
