import os, sys, django
sys.path.extend([os.path.abspath(os.path.dirname(os.path.dirname(__file__)))])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'app.settings')
django.setup()

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from personnel.models import UserProfile
from media.models import OriginMedia
from django.core.files import File

def init_group_and_permission():
    user = ContentType.objects.get(model='user', app_label='auth')

    add_media, created = Permission.objects.get_or_create(
        content_type=user, codename='add_media', name="Can add new media")
    update_media, created = Permission.objects.get_or_create(
        content_type=user, codename='update_media', name='Can update existing media')
    query_media, created = Permission.objects.get_or_create(
        content_type=user, codename='query_media', name='Can query existing media')
    profile, created = Permission.objects.get_or_create(
        content_type=user, codename='profile', name='Have user profile')
    audio, created = Permission.objects.get_or_create(
        content_type=user, codename='audio', name='Have user audio')

    manager,created = Group.objects.get_or_create(name='manager')
    manager.permissions.add(add_media)
    manager.permissions.add(query_media)
    manager.permissions.add(update_media)
    manager.save()

    visitor, created = Group.objects.get_or_create(name='visitor')
    visitor.permissions.add(query_media)
    visitor.permissions.add(profile)
    visitor.permissions.add(audio)
    visitor.save()

def create_superuser():
    try:
        admin = User.objects.create_superuser(username='admin', password='123456')
    except:
        admin = User.objects.get(username='admin')
    profile, created = UserProfile.objects.get_or_create(user=admin, openid='123456')
    profile.save()


create_superuser()
init_group_and_permission()

media = OriginMedia(level_id=1)
with open('E:/Voice test game/data/test/大碗宽面.wav', 'rb') as f:
    media.audio_path.save(name='大碗宽面.wav', content=File(f))

with open('E:/Voice test game/data/test/大碗宽面.mp4', 'rb') as f:
    media.video_path.save(name='大碗宽面.mp4', content=File(f))