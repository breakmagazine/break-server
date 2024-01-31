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
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from breakserver.settings import secrets
from .adapter import CustomKakaoOAuth2Adapter
from .models import CustomUser
from .serializers import CustomUserSerializer

BASE_URL = 'http://127.0.0.1:8000/'
KAKAO_CALLBACK_URI = BASE_URL + 'accounts/kakao/callback/'
REST_API_KEY = getattr(settings, 'KAKAO_REST_API_KEY')
CLIENT_SECRET = secrets['SECRET_KEY']

# Kakao API 요청 함수
def get_kakao_token(code):
    try:
        response = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&client_secret={CLIENT_SECRET}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}"
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise e


# Kakao 프로필 정보 요청 함수
def get_kakao_profile(access_token):
    try:
        response = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise e

class SocialLoginView(APIView):

    @extend_schema(
        summary="카카오 로그인",
        description="카카오 로그인 페이지로 리다이렉트합니다.",
        responses={302: OpenApiResponse(description="Redirects to the Kakao login page.", response=None)}
    )
    @api_view(['GET'])
    @permission_classes([AllowAny])
    def kakao_login(request):
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
        )

    @extend_schema(exclude=True)
    @api_view(['GET'])
    @permission_classes([AllowAny])
    def kakao_callback(request):
        # Access Token Request
        try:
            code = request.GET.get("code")
            token_data = get_kakao_token(code)
            access_token = token_data.get("access_token")
            refresh_token = token_data.get("refresh_token")

            # Profile Request
            profile_data = get_kakao_profile(access_token)
            user_oid = profile_data.get('id')
            kakao_account = profile_data.get('kakao_account')
            nickname = kakao_account['profile']['nickname']
            profile_image_url = kakao_account['profile']['profile_image_url']

            # Signup or Signin Request
            try:
                user = CustomUser.objects.get(oid=user_oid)
                serializer = CustomUserSerializer(user)
                response_data = serializer.data
                response_data.update({
                    'access_token': access_token,
                    'refresh_token': refresh_token
                })
                return Response(response_data)

            except CustomUser.DoesNotExist:
                # 기존에 가입된 유저가 없으면 새로 가입
                data = {'access_token': access_token, 'code': code, 'id_token': user_oid}

                accept = requests.post(
                    f"{BASE_URL}accounts/kakao/login/finish/",
                    data=data,
                )

                accept_status = accept.status_code
                if accept_status != 200:
                    return Response({'err_msg': 'failed to signup'}, status=accept_status)

                with transaction.atomic():
                    user = CustomUser.objects.create(
                        oid=user_oid,
                        username=nickname,
                        profileImage=profile_image_url,
                        position=None,
                        directNumber=None,
                        status='Pending'
                    )

                serializer = CustomUserSerializer(user)
                response_data = serializer.data
                response_data.update({
                    'access_token': access_token,
                    'refresh_token': refresh_token
                })

                return Response(response_data)

        except JSONDecodeError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class KakaoLogin(SocialLoginView):
    adapter_class = CustomKakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI

class UpdateUserInfoView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능하도록 설정

    @extend_schema(request=CustomUserSerializer, responses={200: CustomUserSerializer})
    def put(self, request, *args, **kwargs):
        user = request.user


        # 유저 데이터 가져옴
        nickname = request.data.get('nickname')
        profile_image = request.data.get('profileImage')
        position = request.data.get('position')
        direct_number = request.data.get('directNumber')
        status = request.data.get('status')

        # 유저 데이터 비교
        user.username = nickname if nickname is not None else user.username
        user.profileImage = profile_image if profile_image is not None else user.profileImage
        user.position = position if position is not None else user.position
        user.directNumber = direct_number if direct_number is not None else user.directNumber
        user.status = status if status is not None else user.status
        user.save()

        # 업데이트된 사용자 정보를 반환
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


