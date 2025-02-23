from rest_framework import serializers
from .models import RemarkablePlace


class RemarkablePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemarkablePlace
        fields = ['id', 'name', 'location', 'rating']