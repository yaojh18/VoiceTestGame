"""
Register urls here.
"""
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, WechatViewSet, LevelViewSet

router = DefaultRouter()
router.register('users',UserViewSet, basename='users')
router.register('wechat',WechatViewSet, basename='wechat')
router.register('level', LevelViewSet, basename='level')

urlpatterns = [

]
urlpatterns += router.urls
