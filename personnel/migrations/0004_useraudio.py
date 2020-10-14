# Generated by Django 3.0.8 on 2020-10-14 02:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('media', '0001_initial'),
        ('personnel', '0003_auto_20201013_2328'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAudio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_path', models.FileField(upload_to='users/audio')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('score', models.IntegerField(default=0)),
                ('audio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='media.OriginMedia')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audios', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
