from rest_framework import viewsets, mixins
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from .models import Post, Follow, Group
from .serializers import PostSerializer, CommentSerializer, FollowSerializer, GroupSerializer
from django.shortcuts import get_object_or_404
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, 
                          IsOwnerOrReadOnly)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']

  
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwnerOrReadOnly)


    def get_queryset(self):
        post_id=self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        return post.comments

    def perform_create(self, serializer):
        post_id=self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user)


class FollowAndGroup(viewsets.ModelViewSet,
                    mixins.CreateModelMixin, 
                    mixins.ListModelMixin):
    http_method_names = ['get', 'post']


class FollowViewSet(FollowAndGroup):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['=following__username', '=user__username']
    filterset_fields = ['user']


    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(following__username=user.username)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GroupViewSet(FollowAndGroup):
    serializer_class = GroupSerializer


    def get_queryset(self):
        return Group.objects.all()