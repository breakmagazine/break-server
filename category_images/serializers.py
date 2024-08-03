from rest_framework import serializers
from .models import CategoryImage

class CategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryImage
        fields = ['category', 'image_url']