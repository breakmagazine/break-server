from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import MainBanner, CentralBanner
from .serializers import MainBannerSerializer, CentralBannerSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample


class MainBannerView(APIView):
    @extend_schema(
        summary="메인 배너 반환",
        description="메인 배너 5개를 반환합니다.",
    )
    def get(self, request):
        try:
            banner = MainBanner.objects.get(pk=1)
        except MainBanner.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MainBannerSerializer(banner)
        return Response(serializer.data)

    @extend_schema(
        summary="메인 배너 업데이트",
        description="메인 배너 5개의 URL을 업데이트합니다.",
        request=MainBannerSerializer
    )
    def put(self, request):
        try:
            banner = MainBanner.objects.get(pk=1)
        except MainBanner.DoesNotExist:
            banner = MainBanner(pk=1)

        serializer = MainBannerSerializer(banner, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CentralBannerView(APIView):
    @extend_schema(
        summary="중앙 배너 반환",
        description="중앙 배너를 반환합니다.",
    )
    def get(self, request):
        try:
            banner = CentralBanner.objects.get(pk=1)
        except CentralBanner.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CentralBannerSerializer(banner)
        return Response(serializer.data)

    @extend_schema(
        summary="중앙 배너 업데이트",
        description="중앙 배너의 URL을 업데이트합니다.",
        request=CentralBannerSerializer
    )
    def put(self, request):
        try:
            banner = CentralBanner.objects.get(pk=1)
        except CentralBanner.DoesNotExist:
            banner = CentralBanner(pk=1)

        serializer = CentralBannerSerializer(banner, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)