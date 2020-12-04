from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, GroupList, FollowViewSet
from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )

v1_router = DefaultRouter()
v1_router.register('posts', PostViewSet, basename = 'post')
v1_router.register('posts/(?P<post_id>.+)/comments', CommentViewSet, basename = 'comment')
v1_router.register('follow', FollowViewSet, basename = 'follow')

urlpatterns = [
        path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('group/', GroupList.as_view()),
    ] + v1_router.urls
