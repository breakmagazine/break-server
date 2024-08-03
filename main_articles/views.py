from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import MainArticle
from .serializers import MainArticleSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample


class MainArticleView(APIView):
    @extend_schema(
        summary="MainArticle 반환",
        description="MainArticle 정보를 반환합니다.",
    )
    def get(self, request):
        try:
            main_article = MainArticle.objects.get(pk=1)
        except MainArticle.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MainArticleSerializer(main_article)
        return Response(serializer.data)

    @extend_schema(
        summary="MainArticle 업데이트",
        description="MainArticle 정보를 업데이트합니다.",
        request=MainArticleSerializer
    )
    def put(self, request):
        try:
            main_article = MainArticle.objects.get(pk=1)
        except MainArticle.DoesNotExist:
            main_article = MainArticle(pk=1)

        serializer = MainArticleSerializer(main_article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)