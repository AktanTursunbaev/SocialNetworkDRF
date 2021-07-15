from rest_framework import serializers
from api.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "title", "content", "user")
        read_only_fields = ("id", "user")

    def create(self, validated_data):
        user = validated_data.get("user")
        instance = Post.objects.create(
            title=validated_data["title"], content=validated_data["content"], user=user
        )
        validated_data["id"] = instance.id
        return validated_data
