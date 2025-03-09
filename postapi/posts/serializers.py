import json
from rest_framework import serializers
from .models import Post
from .fields import JSONListField

class PostSerializer(serializers.ModelSerializer):
    keywords = JSONListField()

    class Meta:
        model = Post
        fields = (
            'id', 'name', 'description', 'keywords', 'url',
            'author_ip', 'created_at', 'updated_at'
        )
        read_only_fields = ('author_ip', 'created_at', 'updated_at')

    def validate(self, data):
        name = data.get('name')
        keywords = data.get('keywords', [])

        if len(set(keywords)) < 3:
            raise serializers.ValidationError("At least 3 unique keywords are required.")

        if name in keywords:
            raise serializers.ValidationError("The name must not be one of the keywords.")

        total_length = sum(len(word) for word in keywords) + max(0, len(keywords) - 1)
        if total_length > 500:
            raise serializers.ValidationError("The combined length of keywords exceeds 500 characters.")

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        ip = request.META.get('REMOTE_ADDR') if request else None
        validated_data['author_ip'] = ip
        keywords_list = validated_data.pop('keywords')
        validated_data['keywords'] = json.dumps(keywords_list)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'keywords' in validated_data:
            keywords_list = validated_data.pop('keywords')
            validated_data['keywords'] = json.dumps(keywords_list)
        return super().update(instance, validated_data)
