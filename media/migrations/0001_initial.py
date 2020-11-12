# Generated by Django 3.0.8 on 2020-11-12 10:45

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
                ('level_id', models.IntegerField(db_index=True)),
                ('speaker_id', models.CharField(max_length=64, null=True)),
                ('type_id', models.IntegerField(choices=[(0, 'Unknown'), (1, 'Male'), (2, 'Female')], default=0)),
                ('title', models.CharField(max_length=128)),
                ('content', models.CharField(max_length=1024)),
                ('audio_path', models.FileField(max_length=256, upload_to='origin/audio/')),
                ('video_path', models.FileField(max_length=256, upload_to='origin/video/')),
            ],
        ),
        migrations.AddConstraint(
            model_name='originmedia',
            constraint=models.UniqueConstraint(fields=('level_id', 'type_id'), name='unique_level'),
        ),
    ]
