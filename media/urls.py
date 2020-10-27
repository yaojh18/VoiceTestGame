"""
urls for media app
"""
from rest_framework.routers import DefaultRouter
from .views import ManagerViewSets, ClientMediaViewSets

router = DefaultRouter()
router.register('manager', ManagerViewSets, basename='manager')
router.register('media', ClientMediaViewSets, basename='media')

urlpatterns = []
urlpatterns += router.urls
