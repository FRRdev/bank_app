from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Currency, Category, Transaction, Bank
from .serializers import CurrencySerializer, CategorySerializer, WriteTransactionSerializer, \
    ReadTransactionSerializer, ReportEntrySerializer, ReportParamsSerializer, BankWriteSerializer, BankReadSerializer

from src.profiles.models import UserNet
from .reports import transaction_report
from .permissions import IsAdminOrReadOnly, AllowListPermission
from src.base.classes import MixedPermission, CreateRetrieveUpdateDestroy


class CurrencyModelViewSet(ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    pagination_class = None


class CategoryModelViewSet(ModelViewSet):
    permission_classes = (AllowListPermission,)
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class TransactionModelViewSet(ModelViewSet):
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ("description",)
    ordering_fields = ("amount", "date")
    filterset_fields = ("currency__code",)

    def get_queryset(self):
        return Transaction.objects.select_related("currency", "category", "user").filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        possibility_to_save = Bank.objects.prefetch_related("bank_users", "currencies").filter(
            bank_users=request.user.pk, currencies=serializer.validated_data['currency'])
        if possibility_to_save:
            print('Транзакция возможна')
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return HttpResponse('Incorrect transactions.Please input correct currency.')

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadTransactionSerializer
        return WriteTransactionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionReportAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        params_serializer = ReportParamsSerializer(data=request.GET, context={"request": request})
        params_serializer.is_valid(raise_exception=True)
        params = params_serializer.save()

        data = transaction_report(params)
        serializer = ReportEntrySerializer(instance=data, many=True)
        return Response(data=serializer.data)


class BankView(MixedPermission, ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankWriteSerializer
    permission_classes_by_action = {'list': [IsAuthenticated],
                                    'create': [IsAdminUser],
                                    'update': [IsAuthenticated],
                                    'destroy': [IsAuthenticated]}

    def get_queryset(self):
        return Bank.objects.prefetch_related("currencies", "bank_users").all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BankReadSerializer
        return BankWriteSerializer

