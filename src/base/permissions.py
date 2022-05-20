from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
from src.bank_core.models import AllowList


class IsMemberGroup(BasePermission):
    """ Участик группы или админимтратор
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.group.members.all() or obj.group.founder == request.user


class IsAuthorEntry(BasePermission):
    """ Автор записи или админимтратор
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or obj.group.founder == request.user


class IsAuthorCommentEntry(BasePermission):
    """ Автор комментария или админимтратор
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or obj.entry.group.founder == request.user


class IsAuthor(BasePermission):
    """ Автор комментария или записи
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAdminOrReadOnly(BasePermission):
    """ Проверка на staff или readonly
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            request.user.is_staff,
        )


class AllowListPermission(BasePermission):
    """ Проверка допустимого ip адресса
    """
    def has_permission(self, request, view):
        ip_addr = request.META['REMOTE_ADDR']
        allowed = AllowList.objects.filter(ip_address=ip_addr).exists()
        return allowed
