from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CategoryImage
from .serializers import CategoryImageSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample


class CategoryImageView(APIView):
    @extend_schema(
        summary="카테고리 이미지 반환",
        description="지정된 카테고리의 이미지를 반환합니다.",
        responses=CategoryImageSerializer
    )
    def get(self, request, category):
        try:
            category_image = CategoryImage.objects.get(category=category.upper())
        except CategoryImage.DoesNotExist:
            return Response({"detail": "해당 카테고리의 이미지를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategoryImageSerializer(category_image)
        return Response(serializer.data)

    @extend_schema(
        summary="카테고리 이미지 업데이트",
        description="지정된 카테고리의 이미지를 업데이트합니다. -- 진짜 미안한데 category에 같은거 한번씩 적어주라...",
        request=CategoryImageSerializer,
        responses=CategoryImageSerializer
    )
    def put(self, request, category):
        category = category.upper()
        try:
            category_image = CategoryImage.objects.get(category=category)
        except CategoryImage.DoesNotExist:
            category_image = CategoryImage(category=category)

        serializer = CategoryImageSerializer(category_image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)