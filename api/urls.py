from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet
from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )

v1_router = routers.DefaultRouter()
v1_router.register('v1/posts', PostViewSet, basename = 'post')
v1_router.register('v1/posts/(?P<post_id>.+)/comments', CommentViewSet, basename = 'comment')
v1_router.register('v1/follow', FollowViewSet, basename = 'follow')
v1_router.register('v1/group', GroupViewSet, basename = 'group')

urlpatterns = [
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(v1_router.urls))
    ]