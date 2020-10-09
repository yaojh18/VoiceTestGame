"""
Register urls here.
"""
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, WechatViewSet

router = DefaultRouter()
router.register('users',UserViewSet, basename='users')
router.register('wechat',WechatViewSet, basename='wechat')

urlpatterns = [

]
urlpatterns += router.urls
