from rest_framework import serializers
from .models import PropertyComment, UserComment

class PropertyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyComment
        fields = '__all__'

class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserComment
        fields = '__all__'