from django.urls import path
from . import views

urlpatterns = [
    path('result/', views.Result.as_view(), name='result'),
]