"""
urls for media app
"""
from rest_framework.routers import DefaultRouter
import media.views as views

router = DefaultRouter()
router.register('manager', views.ManagerViewSets, basename='manager')
router.register('media', views.ClientMediaViewSets, basename='media')
router.register('manager/data/user', views.UserDataViewSets, basename='manager/data/user')
router.register('manager/data/user_audio', views.UserAudioDataViewSets,
                basename='manager/data/user_audio')
router.register('manager/data/origin', views.MediaDataViewSets, basename='manager/data/origin')

urlpatterns = []
urlpatterns += router.urls
