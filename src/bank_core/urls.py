from django.urls import path
from rest_framework import routers

from src.bank_core import views

router = routers.SimpleRouter()

# router.register(r'categories', views.CategoryModelViewSet, basename="category")
# router.register(r'transactions', views.TransactionModelViewSet, basename="transaction")
# router.register(r"currencies", views.CurrencyModelViewSet, basename="currency")

urlpatterns = router.urls