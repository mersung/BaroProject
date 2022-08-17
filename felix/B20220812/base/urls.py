from django.contrib import admin
from django.urls import path, include

from .views import changed, fixed, refresh

urlpatterns = [
    path('fixed/', fixed, name='fixed'),
    path('changed/', changed, name='changed'),
    # path('refresh/', refresh, name='refresh')
]
