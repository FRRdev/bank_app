from rest_framework import permissions, viewsets
from rest_framework.response import Response

from src.base.classes import MixedPermission
from src.wall.serializers import ListPostSerializer, PostSerializer
from .services import feed_services


class FeedView(viewsets.GenericViewSet):
    """ View follower's feed
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ListPostSerializer

    def list(self, request, *args, **kwargs):
        queryset = feed_services.get_post_list(request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = feed_services.get_single_post(kwargs.get('pk'))
        serializer = PostSerializer(instance)
        return Response(serializer.data)

