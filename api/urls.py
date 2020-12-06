from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers, viewsets
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PostViewSet, CommentViewSet, GroupList, FollowViewSet
from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )

# признаюсь, данный кастомный роутер я делал не сам, а нашел на stackoverflow...
# наверняка, без этого можно было обойтись
class DefaultRouterWithSimpleViews(routers.DefaultRouter):


    def get_routes(self, viewset):
        if issubclass(viewset, viewsets.ViewSetMixin):
            return super(DefaultRouterWithSimpleViews, self).get_routes(viewset)
        return []

    def get_urls(self):
        ret = []
        for prefix, viewset, basename in self.registry:
            if issubclass(viewset, viewsets.ViewSetMixin):
                continue
            regex = '{prefix}{trailing_slash}$'.format(
                prefix=prefix,
                trailing_slash=self.trailing_slash
            )
            ret.append(url(
                regex, viewset.as_view(),
                name='{0}-list'.format(basename)
            ))
        ret = format_suffix_patterns(ret, allowed=['json', 'html'])
        return super(DefaultRouterWithSimpleViews, self).get_urls() + ret


v1_router = DefaultRouterWithSimpleViews()
v1_router.register('posts', PostViewSet, basename = 'post')
v1_router.register('posts/(?P<post_id>.+)/comments', CommentViewSet, basename = 'comment')
v1_router.register('follow', FollowViewSet, basename = 'follow')
v1_router.register('group', GroupList, basename = 'group')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(v1_router.urls))
    ]