import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

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

    manager,created = Group.objects.get_or_create(name='manager')
    manager.permissions.add(add_media)
    manager.permissions.add(query_media)
    manager.permissions.add(update_media)
    manager.save()

    visitor, created = Group.objects.get_or_create(name='visitor')
    visitor.permissions.add(query_media)
    visitor.permissions.add(profile)
    visitor.save()

init_group_and_permission()