from urllib.request import Request

from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiResponse

import requests
from django.shortcuts import redirect, get_object_or_404
from django.conf import settings
from json.decoder import JSONDecodeError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from breakserver.settings import secrets

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_view
from .models import CustomUser
from .serializers import UserLoginSerializer

BASE_URL = "http://127.0.0.1:8000/"
KAKAO_CALLBACK_URI = BASE_URL + "accounts/kakao/callback/"
REST_API_KEY = getattr(settings, "KAKAO_REST_API_KEY")
CLIENT_SECRET = secrets["SECRET_KEY"]


@extend_schema(
    summary="카카오 로그인",
    description="카카오 로그인 페이지로 리다이렉트합니다.",
    responses={
        302: OpenApiResponse(
            description="Redirects to the Kakao login page.", response=None
        )
    },
)
@api_view(["GET"])
@permission_classes([AllowAny])
def kakao_login(request):
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )

@extend_schema(exclude=True)
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def kakao_callback(request):
    code = request.GET.get("code")
    print(code)

    # Access Token Request

    token_req = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&client_secret={CLIENT_SECRET}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}"
    )

    token_req_json = token_req.json()

    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)

    access_token = token_req_json.get("access_token")

    # Email Request

    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_data = profile_request.json()

    kakao_oid = profile_data.get("id")
    kakao_account = profile_data.get("kakao_account")
    username = kakao_account["profile"]["nickname"]
    profile_image_url = kakao_account["profile"]["profile_image_url"]
    email = kakao_account.get("email")

    # 회원가입, 로그인 로직

    data = {"access_token": access_token, "code": code}
    print(data)

    try:
        user = CustomUser.objects.get(email=email)

        accept = requests.post(f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return Response({"err_msg": "failed to signin"}, status=accept_status)

        accept_json = accept.json()
        accept_json.pop("user", None)
        return Response(accept_json)

    except CustomUser.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        with transaction.atomic():
            CustomUser.objects.create(
                email=email,
                kakao_oid=kakao_oid,
                username=username,
                profile_image=profile_image_url,
                position=None,
                direct_number=None,
                status="Pending",
            )

        accept = requests.post(f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return Response({"err_msg": "failed to signup"}, status=accept_status)

        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
        accept_json = accept.json()
        accept_json.pop("user", None)
        return Response(accept_json)

class KakaoLoginView(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UpdateUserInfoView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능하도록 설정

    @extend_schema(request=UserLoginSerializer, responses={200: UserLoginSerializer})
    def put(self, request, *args, **kwargs):
        user = request.user

        # 유저 데이터 가져옴
        nickname = request.data.get("nickname")
        profile_image = request.data.get("profileImage")
        position = request.data.get("position")
        direct_number = request.data.get("directNumber")
        status = request.data.get("status")

        # 유저 데이터 비교
        user.username = nickname if nickname is not None else user.username
        user.profileImage = (
            profile_image if profile_image is not None else user.profileImage
        )
        user.position = position if position is not None else user.position
        user.directNumber = (
            direct_number if direct_number is not None else user.directNumber
        )
        user.status = status if status is not None else user.status
        user.save()

        # 업데이트된 사용자 정보를 반환
        serializer = UserLoginSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
