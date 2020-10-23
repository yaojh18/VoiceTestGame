# Generated by Django 3.0.8 on 2020-10-23 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OriginMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level_id', models.IntegerField(db_index=True, unique=True)),
                ('title', models.CharField(max_length=128)),
                ('content', models.CharField(max_length=1024)),
                ('audio_path', models.FileField(max_length=256, upload_to='origin/audio/')),
                ('video_path', models.FileField(max_length=256, upload_to='origin/video/')),
            ],
        ),
    ]
