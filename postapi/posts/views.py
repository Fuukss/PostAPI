import json
from rest_framework import viewsets
from .models import Post, PostHistory
from .serializers import PostSerializer
from .permissions import IsOwnerIP

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerIP]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        snapshot = {
            "name": instance.name,
            "description": instance.description,
            "keywords": json.loads(instance.keywords) if isinstance(instance.keywords, str) else instance.keywords,
            "url": instance.url,
        }
        response = super().update(request, *args, **kwargs)
        PostHistory.objects.create(
            post=instance,
            operation="update",
            data=snapshot,
            modified_by_ip=request.META.get('REMOTE_ADDR')
        )
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        snapshot = {
            "name": instance.name,
            "description": instance.description,
            "keywords": json.loads(instance.keywords) if isinstance(instance.keywords, str) else instance.keywords,
            "url": instance.url,
        }
        PostHistory.objects.create(
            post=instance,
            original_post_id=instance.id,
            operation="delete",
            data=snapshot,
            modified_by_ip=request.META.get('REMOTE_ADDR')
        )
        return super().destroy(request, *args, **kwargs)
