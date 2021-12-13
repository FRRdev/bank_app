from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import UserNet, Technology
from .serializers import GetUserNetSerializer, GetUserPublicSerializer, TechnologySerializer, \
    GetUserNetReadableSerializer
from ..base.classes import CreateRetrieveUpdateDestroy


class UserNetPublicView(ModelViewSet):
    """Вывод публичного профиля"""
    queryset = UserNet.objects.all()
    serializer_class = GetUserPublicSerializer
    permission_classes = [permissions.AllowAny]


class UserNetView(ModelViewSet):
    """Вывод профиля"""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserNet.objects.filter(id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GetUserNetReadableSerializer
        else:
            return GetUserNetSerializer


class TechnologyView(CreateRetrieveUpdateDestroy):
    """ CRUD технологии """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer

    permission_classes_by_action = {'get': [permissions.AllowAny],
                                    'update': [permissions.IsAuthenticated],
                                    'destroy': [permissions.IsAuthenticated]}
