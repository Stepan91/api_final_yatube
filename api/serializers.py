from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Post, Comment, Group, Follow, User
from rest_framework.fields import CurrentUserDefault


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('id', 'title',)
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
                        slug_field='username',
                        read_only=True,
                        default = CurrentUserDefault()
                        )
    following = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())


    def validate(self, data):
        user = self.context['request'].user
        following = data['following']
        check_follow = Follow.objects.filter(user=user, following=following)
        if user == following:
            raise serializers.ValidationError("Подписка самого на себя невозможна!")
        if check_follow.exists():
            raise serializers.ValidationError("Подписка уже создана!")
        return data

    class Meta:
        fields = ('user', 'following',)
        model = Follow
        # сделал валидацию такой сначала, 
        # но тест на уже подписанного автора не проходил
        """ validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(), 
                fields=('user', 'following')
                )
        ] """
        validators = []