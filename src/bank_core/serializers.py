from src.profiles.models import UserNet
from rest_framework import serializers
from django.db.models import Sum

from .models import Currency, Category, Transaction, Bank
from .reports import ReportParams
from src.profiles.serializers import GetUserBankSerializer


class ReadUserSerializer(serializers.ModelSerializer):
    """ Serializer for public user info
    """

    class Meta:
        model = UserNet
        fields = ("id", "username", "first_name", "last_name")
        read_only_fields = fields


class CurrencySerializer(serializers.ModelSerializer):
    """ Serializer for Currency
    """

    class Meta:
        model = Currency
        fields = ("id", "code", "name", "bank")


class CategorySerializer(serializers.ModelSerializer):
    """ Serializer for Category
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = ("id", "name", "user")


class WriteTransactionSerializer(serializers.ModelSerializer):
    """ Serializer to write transaction
    """

    # currency = serializers.SlugRelatedField(slug_field="code", queryset=Currency.objects.all())

    class Meta:
        model = Transaction
        fields = ("amount", "currency", "date", "description", "category")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        self.fields['category'].queryset = user.categories.all()


class ReadTransactionSerializer(serializers.ModelSerializer):
    """ Serializer to read transaction
    """
    user = ReadUserSerializer()
    currency = CurrencySerializer()
    category = CategorySerializer()

    class Meta:
        model = Transaction
        fields = ("id", "amount", "currency", "date", "description", "category", "user")
        read_only_fields = fields


class ReportEntrySerializer(serializers.Serializer):
    """ Serializer for report about transaction
    """
    category = CategorySerializer()
    total = serializers.DecimalField(max_digits=15, decimal_places=2)
    count = serializers.IntegerField()
    avg = serializers.DecimalField(max_digits=15, decimal_places=2)


class ReportParamsSerializer(serializers.Serializer):
    """ Serializer for parameters for report
    """
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        return ReportParams(**validated_data)


class BankWriteSerializer(serializers.ModelSerializer):
    """ Serializer to write bank
    """
    bank_users = GetUserBankSerializer(many=True, read_only=True)
    currencies = CurrencySerializer(many=True, read_only=True)

    class Meta:
        model = Bank
        fields = '__all__'


class BankReadSerializer(serializers.ModelSerializer):
    """ Serializer to read bank
    """
    total_sum_of_transaction = serializers.SerializerMethodField('get_total_sum_of_transaction')
    bank_users = GetUserBankSerializer(many=True, read_only=True)
    currencies = CurrencySerializer(many=True, read_only=True)

    class Meta:
        model = Bank
        fields = '__all__'

    def get_total_sum_of_transaction(self, obj):
        query_result = Transaction.objects.select_related("user").filter(user__bank=obj.pk).aggregate(
            total_sum=Sum('amount'))
        return query_result['total_sum']
