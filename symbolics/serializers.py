from rest_framework import serializers
from .models import Symbolic

class SymbolicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbolic
        fields = ['symbolic_image', 'title', 'content']