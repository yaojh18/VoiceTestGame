"""
urls for media app
"""
from rest_framework.routers import DefaultRouter
from .views import ManagerViewSets, ClientViewSets

router = DefaultRouter()
router.register('manager', ManagerViewSets, basename='manager')
router.register('client', ClientViewSets, basename='client')

urlpatterns = []
urlpatterns += router.urls
