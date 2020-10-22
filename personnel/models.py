"""
Models for personnel.
"""
# pylint: disable=E5142
from django.db import models
from django.contrib.auth.models import User
from media.models import OriginMedia

# Create your models here.


class UserProfile(models.Model):
    """
    Add information for User.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    openid = models.CharField(max_length=128, null=True, unique=True)
    gender = models.CharField(max_length=32, null=True)
    city = models.CharField(max_length=128, null=True)
    province = models.CharField(max_length=128, null=True)
    level = models.IntegerField(default=0)
    avatar_url = models.CharField(max_length=128, null=True)


class UserAudio(models.Model):
    """
    User audio information, identified by timestamp.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audios')
    media = models.ForeignKey(OriginMedia, on_delete=models.CASCADE, related_name='users')
    audio = models.FileField(max_length=512, upload_to='users/audio')
    timestamp = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)

    def get_audio_name(self):
        """
        Uniform way to name a file.
        """
        return self.user.username + '_' + str(self.media.title) + '.wav'
