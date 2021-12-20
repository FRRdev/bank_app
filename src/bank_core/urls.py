from django.urls import path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register(r'categories', views.CategoryModelViewSet, basename="category")
router.register(r'transactions', views.TransactionModelViewSet, basename="transaction")
router.register(r"currencies", views.CurrencyModelViewSet, basename="currency")
router.register(r"bank", views.BankView, basename="bank")
urlpatterns = [
                  # path('technology/', views.TechnologyView.as_view({'post': 'create'})),
                  # path('technology/<int:pk>/',
                  #      views.TechnologyView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}))
                  path("report/", views.TransactionReportAPIView.as_view(), name="report"),
              ] + router.urls
