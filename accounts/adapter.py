from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
import requests
from allauth.socialaccount.providers.kakao.provider import KakaoProvider

from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

class CustomKakaoOAuth2Adapter(OAuth2Adapter):
    provider_id = KakaoProvider.id
    access_token_url = "https://kauth.kakao.com/oauth/token"
    authorize_url = "https://kauth.kakao.com/oauth/authorize"
    profile_url = "https://kapi.kakao.com/v2/user/me"

    def complete_login(self, request, app, token, **kwargs):
        headers = {"Authorization": "Bearer {0}".format(token.token)}
        resp = requests.get(self.profile_url, headers=headers)
        resp.raise_for_status()
        extra_data = resp.json()
        # print(extra_data)
        user_oid = extra_data.get('id')
        profile_image = extra_data.get('properties', {}).get('profile_image')

        return self.get_provider().sociallogin_from_response(request, extra_data)

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super(CustomSocialAccountAdapter, self).save_user(request, sociallogin, form)
        print(sociallogin)

        # user.oid = sociallogin.account.extra_data.get('id')
        # user.profileImage = sociallogin.account.extra_data.get('properties', {}).get('profile_image')
        # print(user.profileImage)
        # print("save_user called")
        # user.save()
        #
        # return user
