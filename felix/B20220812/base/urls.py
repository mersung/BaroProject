from django.contrib import admin
from django.urls import path

from .views import changed, fixed, index

urlpatterns = [
    path('fixed/', fixed, name='fixed'),
    path('changed/', changed, name='changed'),
    path('', index, name='index')
    # path('refresh/', refresh, name='refresh')
]
