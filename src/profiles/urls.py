from django.urls import path
from . import views

urlpatterns = [
    path('technology/', views.TechnologyView.as_view({'post': 'create'})),
    path('technology/<int:pk>/',
         views.TechnologyView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('profile/<int:pk>/', views.UserNetView.as_view({'get': 'retrieve', 'put': 'update'})),
    path('<int:pk>/', views.UserNetPublicView.as_view({'get': 'retrieve'})),
]
