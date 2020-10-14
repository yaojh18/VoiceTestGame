"""
urls for media app
"""
from rest_framework.routers import DefaultRouter
from .views import ManagerViewSets

router = DefaultRouter()
router.register('manager', ManagerViewSets, basename='manager')

urlpatterns = []
urlpatterns += router.urls
