from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import History
from .serializers import HistorySerializer
from drf_spectacular.utils import extend_schema, OpenApiExample


class HistoryListCreateView(generics.ListCreateAPIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

    @extend_schema(
        summary="History 목록 및 생성",
        description="모든 History를 반환하거나 새로운 History를 생성합니다.",
        request=HistorySerializer
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class HistoryDetailView(APIView):
    @extend_schema(
        summary="History 조회",
        description="특정 History를 조회합니다.",
    )
    def get(self, request, pk):
        try:
            history = History.objects.get(publication_number=pk)
        except History.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = HistorySerializer(history)
        return Response(serializer.data)

    @extend_schema(
        summary="History 업데이트",
        description="특정 History를 업데이트합니다.",
        request=HistorySerializer
    )
    def put(self, request, pk):
        try:
            history = History.objects.get(pk=pk)
        except History.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = HistorySerializer(history, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)