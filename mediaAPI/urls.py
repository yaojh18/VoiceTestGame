from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('manager', ManagerViewSets, basename='manager')
router.register('client', ClientViewSets, basename='client')

urlpatterns = []
urlpatterns += router.urls

