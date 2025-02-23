# serializers.py
from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'main_image', 'preview_image', 'content', 'publication_date', 'author']