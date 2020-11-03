"""
urls for media app
"""
from rest_framework.routers import DefaultRouter
import media.views as views

router = DefaultRouter()
router.register('manager', views.ManagerViewSets, basename='manager')
router.register('media', views.ClientMediaViewSets, basename='media')
router.register('manager/analysis/user', views.UserDataViewSets, basename='manager/analysis/user')
router.register('manager/analysis/user_audio', views.UserAudioDataViewSets, basename='manager/analysis/user_audio')
router.register('manager/analysis/origin', views.MediaDataViewSets, basename='manager/analysis/origin')
# router.register('manager/data', views.DataViewSets, basename='manager/data')

urlpatterns = []
urlpatterns += router.urls
