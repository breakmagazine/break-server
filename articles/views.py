from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics
from .models import Article
from .serializers import ArticleSerializer, ArticleDetailSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ArticleCreateView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer

    def get(self, request, *args, **kwargs):
        try:
            article = self.get_object()
            serializer = self.get_serializer(article)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    summary="기사 반환",
    description="카테고리를 기반으로 기사를 반환합니다.",
    parameters=[
        OpenApiParameter(
            name="category",
            type=str,
            description="검색을 요청할 카테고리입니다.",
        ),
        OpenApiParameter(
            name="subCategory",
            type=str,
            description="카테고리가 FASHION 일 경우, 검색을 요청할 sub category입니다.",
        ),
    ],
)
class ArticleListByCategoryView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        category = self.request.query_params.get("category", None)
        sub_category = self.request.query_params.get("subCategory", None)

        if category not in [
            "ABOUT",
            "FASHION",
            "FEATURE",
            "PHOTOGRAPHY",
            "FILM",
            "ART",
        ]:
            return (
                Article.objects.none()
            )  # 유효하지 않은 카테고리인 경우 빈 쿼리셋 반환

        if category == "FASHION":
            return Article.objects.filter(category=category, sub_category=sub_category)
        return Article.objects.filter(category=category)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        category = self.request.query_params.get("category", None)

        if category not in [
            "ABOUT",
            "FASHION",
            "FEATURE",
            "PHOTOGRAPHY",
            "FILM",
            "ART",
        ]:
            return Response(
                {"detail": "잘못된 category입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        if category == "FASHION" and not queryset.exists():
            return Response(
                {"detail": "잘못된 sub category입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
