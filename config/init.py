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

    management, created = Permission.objects.get_or_create(
        content_type=user, codename='management', name="Can add new media")
    profile, created = Permission.objects.get_or_create(
        content_type=user, codename='profile', name='Have user profile')
    audio, created = Permission.objects.get_or_create(
        content_type=user, codename='audio', name='Have user audio')

    manager,created = Group.objects.get_or_create(name='manager')
    manager.permissions.add(management)
    manager.permissions.add()
    manager.save()

    visitor, created = Group.objects.get_or_create(name='visitor')
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
