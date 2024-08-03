from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Symbolic
from .serializers import SymbolicSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample


class SymbolicView(APIView):
    @extend_schema(
        summary="Symbolic 반환",
        description="Symbolic 정보를 반환합니다.",
    )
    def get(self, request):
        try:
            symbolic = Symbolic.objects.get(pk=1)
        except Symbolic.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SymbolicSerializer(symbolic)
        return Response(serializer.data)

    @extend_schema(
        summary="Symbolic 업데이트",
        description="Symbolic 정보를 업데이트합니다.",
        request=SymbolicSerializer
    )
    def put(self, request):
        try:
            symbolic = Symbolic.objects.get(pk=1)
        except Symbolic.DoesNotExist:
            symbolic = Symbolic(pk=1)

        serializer = SymbolicSerializer(symbolic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)