from django.shortcuts import render
from django.http import JsonResponse
from utils import create_presigned_post


def kakao_login_page(request):
    return render(request, "home.html")


def get_presigned_url(request):
    if request.method == "GET":
        bucket_name = "breakmagazine_image"
        object_name = request.GET.get(
            "object_name"
        )  # 예: 'articles/thumbnails/your-image.jpg'

        if not object_name:
            return JsonResponse({"error": "Object name is required"}, status=400)

        response = create_presigned_post(bucket_name, object_name)
        if response:
            return JsonResponse(response)
        else:
            return JsonResponse(
                {"error": "Could not generate presigned URL"}, status=500
            )
