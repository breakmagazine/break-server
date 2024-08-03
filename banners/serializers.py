from rest_framework import serializers
from .models import MainBanner, CentralBanner

class MainBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainBanner
        fields = ['banner1', 'banner2', 'banner3', 'banner4', 'banner5']

class CentralBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentralBanner
        fields = ['banner']