from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, permissions
from .models import Article
from .serializers import ArticleSerializer, ArticleDetailSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.exceptions import ValidationError

@extend_schema(
    summary="기사 작성",
    description="기사를 작성합니다.",
    request=ArticleSerializer
)
class ArticleCreateView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        category = serializer.validated_data.get('category', None)
        sub_category = serializer.validated_data.get('sub_category', None)
        valid_categories = ["ABOUT", "FASHION", "FEATURE", "PHOTOGRAPHY", "FILM", "ART"]
        valid_sub_categories = ["FEATURE", "PHOTOGRAPHY", "FILM", "ART"]

        if category not in valid_categories:
            raise ValidationError({"category": "잘못된 category입니다."})
        if category == "FASHION" and sub_category not in valid_sub_categories:
            raise ValidationError({"category": "잘못된 subCategory입니다."})

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


class ArticlePagination(PageNumberPagination):
    page_size = 10  # 한 페이지에 표시할 항목 수
    page_size_query_param = 'page_size'
    max_page_size = 100

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
        OpenApiParameter(
            name="order",
            type=str,
            description="정렬 순서. 'latest' 또는 'oldest' 중 하나.",
        ),
    ],
)
class ArticleListByCategoryView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination

    def get_queryset(self):
        category = self.request.query_params.get("category", None)
        sub_category = self.request.query_params.get("subCategory", None)
        order = self.request.query_params.get("order", "latest")

        if category not in [
            "ABOUT",
            "FASHION",
            "FEATURE",
            "PHOTOGRAPHY",
            "FILM",
            "ART",
        ]:
            return Article.objects.none()  # 유효하지 않은 카테고리인 경우 빈 쿼리셋 반환

        if category == "FASHION":
            queryset = Article.objects.filter(category=category, sub_category=sub_category)
        else:
            queryset = Article.objects.filter(category=category)

        if order == "oldest":
            queryset = queryset.order_by("created_at")
        else:
            queryset = queryset.order_by("-created_at")

        return queryset

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

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ArticleUpdateView(generics.UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['put']

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        # if instance.user != request.user:
        #     raise ValidationError({"detail": "이 게시물을 수정할 권한이 없습니다."})

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class ArticleDeleteView(generics.DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        article = self.get_object()
        # if article.user != request.user:
        #     raise ValidationError({"detail": "이 게시물을 삭제할 권한이 없습니다."})
        return self.destroy(request, *args, **kwargs)