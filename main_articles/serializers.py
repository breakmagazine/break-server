from rest_framework import serializers
from .models import MainArticle

class MainArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainArticle
        fields = [
            'main_article1',
            'main_article2',
            'main_article1_redirect_url',
            'main_article2_redirect_url'
        ]