from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Article
from .serializers import ArticlesListSerializer, ArticleDetailSerializer


class ArticleListView(APIView):
    """Вывод списка статей."""
    def get(self, request):
        article = Article.objects.filter(is_published=True)
        serializer = ArticlesListSerializer(article, many=True)
        return Response(serializer.data)


class ArticleDetailView(APIView):
    """ Статья блога. """
    def get(self, request, pk):
        article = Article.objects.get(id=pk)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)

