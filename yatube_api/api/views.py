from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets

from api.serializers import GroupSerializer, PostSerializer, CommentSerializer

from posts.models import Comment, Group, Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionDenied("Нет прав на изменение поста")
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied("Нет прав на удаление поста")
        super().perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        serializer.save(
            author=self.request.user, post=get_object_or_404(Post, id=post_id)
        )

    def perform_update(self, serializer):
        post_id = self.kwargs.get("post_id")
        if self.request.user != serializer.instance.author:
            raise PermissionDenied("Нет прав на редактирование комментария")
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(Post, id=post_id)
        )

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied("Нет прав на удаление комментария")
        super().perform_destroy(instance)
