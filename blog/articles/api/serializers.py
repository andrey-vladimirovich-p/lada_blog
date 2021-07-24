from rest_framework import serializers
from ..models import Article


class ArticlesListSerializer(serializers.ModelSerializer):
    """ Список статей. """
    category = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = Article
        exclude = ('is_published',)


class ArticleDetailSerializer(serializers.ModelSerializer):
    """ Статья блога. """
    category = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = Article
        exclude = ('is_published',)
