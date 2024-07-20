from django.shortcuts import render
import boto3
from botocore.exceptions import ClientError
from django.http import JsonResponse
from django.conf import settings
import environ
import os
from pathlib import Path
import uuid
from rest_framework.decorators import api_view, schema
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

env = environ.Env(DEBUG=(bool, False))
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


def kakao_login_page(request):
    return render(request, "home.html")


def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL S3 GET request
    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=env("AWS_ACCESS_KEY"),
        aws_secret_access_key=env("AWS_SECRET_ACCESS_KEY"),
        region_name="ap-northeast-2",
    )
    try:
        response = s3_client.generate_presigned_url(
            "put_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        print(e)
        return None

    return response


@extend_schema(
    description="S3에 파일을 업로드하기 위해 presigned url 요청",
    parameters=[
        OpenApiParameter(
            name="category",
            type=str,
            description="presigned_url을 요청할 카테고리입니다.",
            examples=[
                OpenApiExample(
                    "USER/PROFILE_IMAGE",
                    value="USER/PROFILE_IMAGE",
                    description="User profile image upload",
                ),
                OpenApiExample(
                    "BANNER/MAIN", value="BANNER/MAIN", description="Main banner upload"
                ),
                OpenApiExample(
                    "BANNER/MID", value="BANNER/MID", description="Middle banner upload"
                ),
                OpenApiExample(
                    "SYMBOLIC", value="SYMBOLIC", description="Symbolic upload"
                ),
                OpenApiExample(
                    "HOME_ARTICLE/LEFT",
                    value="HOME_ARTICLE/LEFT",
                    description="Left home article upload",
                ),
                OpenApiExample(
                    "HOME_ARTICLE/RIGHT",
                    value="HOME_ARTICLE/RIGHT",
                    description="Right home article upload",
                ),
                OpenApiExample(
                    "CATEGORY/ABOUT",
                    value="CATEGORY/ABOUT",
                    description="Category about image upload",
                ),
                OpenApiExample(
                    "CATEGORY/FASHION",
                    value="CATEGORY/FASHION",
                    description="Category fashion image upload",
                ),
                OpenApiExample(
                    "CATEGORY/FEATURE",
                    value="CATEGORY/FEATURE",
                    description="Category feature image upload",
                ),
                OpenApiExample(
                    "CATEGORY/PHOTOGRAPHY",
                    value="CATEGORY/PHOTOGRAPHY",
                    description="Category photography image upload",
                ),
                OpenApiExample(
                    "CATEGORY/FILM",
                    value="CATEGORY/FILM",
                    description="Category film image upload",
                ),
                OpenApiExample(
                    "CATEGORY/ART",
                    value="CATEGORY/ART",
                    description="Category art image upload",
                ),
                OpenApiExample(
                    "HISTORY", value="HISTORY", description="History upload"
                ),
                OpenApiExample(
                    "ARTICLE", value="ARTICLE", description="Article upload"
                ),
            ],
        )
    ],
    responses={
        200: {
            "description": "The presigned URL and object name",
            "content": {
                "application/json": {
                    "example": {
                        "url": "https://s3.ap-northeast-2.amazonaws.com/breakmagazine_image/articles/thumbnails/123e4567-e89b-12d3-a456-426614174000.jpg",
                        "object_name": "articles/thumbnails/123e4567-e89b-12d3-a456-426614174000.jpg",
                    }
                }
            },
        },
        400: {
            "description": "Category is required",
            "content": {
                "application/json": {"example": {"error": "Category is required"}}
            },
        },
        500: {
            "description": "Could not generate presigned URL",
            "content": {
                "application/json": {
                    "example": {"error": "Could not generate presigned URL"}
                }
            },
        },
    },
)
@api_view(["GET"])
def get_presigned_url(request):
    if request.method == "GET":
        bucket_name = env("AWS_STORAGE_BUCKET_NAME")
        category = request.GET.get("category")  # 예: 'articles/thumbnails'

        if not category:
            return JsonResponse({"error": "Category is required"}, status=400)

        # 고유 객체 이름 생성
        object_name = f"{category}/{uuid.uuid4()}.jpg"
        url = create_presigned_url(bucket_name, object_name)
        object_url = (
            f"https://{bucket_name}.s3.ap-northeast-2.amazonaws.com/{object_name}"
        )
        if url:
            return JsonResponse({"url": url, "objectUrl": object_url})
        else:
            return JsonResponse(
                {"error": "Could not generate presigned URL"}, status=500
            )
