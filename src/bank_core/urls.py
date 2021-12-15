from django.urls import path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register(r'categories', views.CategoryModelViewSet, basename="category")
router.register(r'transactions', views.TransactionModelViewSet, basename="transaction")
router.register(r"currencies", views.CurrencyModelViewSet, basename="currency")
urlpatterns = [
                  path("report/", views.TransactionReportAPIView.as_view(), name="report"),
               ] + router.urls
