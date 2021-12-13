from rest_framework import serializers

from .models import UserNet, Technology


class GetUserNetSerializer(serializers.ModelSerializer):
    """ Вывод инфо о user """
    avatar = serializers.ImageField(read_only=True)

    class Meta:
        model = UserNet
        exclude = ("password", "last_login", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")


class GetUserNetReadableSerializer(serializers.ModelSerializer):
    """ Вывод инфо о user (с именами технологий) """
    technology = serializers.SerializerMethodField('get_technologys')
    avatar = serializers.ImageField(read_only=True)

    class Meta:
        model = UserNet
        exclude = ("password", "last_login", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")

    def get_technologys(self, obj):
        tech_name_list = [tech.name for tech in obj.technology.all()]
        return tech_name_list

class GetUserPublicSerializer(serializers.ModelSerializer):
    """ Вывод публичной инфо о user """

    class Meta:
        model = UserNet
        exclude = (
            "email",
            "password",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
            "phone"
        )


class UserByFollowerSerializer(serializers.ModelSerializer):
    """Сериализация для подписчиков
    """
    avatar = serializers.ImageField(read_only=True)

    class Meta:
        model = UserNet
        fields = ('id', 'username', 'avatar')


class TechnologySerializer(serializers.ModelSerializer):
    """Сериализация для технологий пользователя
    """

    class Meta:
        model = Technology
        fields = ('name',)
