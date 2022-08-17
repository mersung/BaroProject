from django.urls import path

from . import views

urlpatterns = [
    path('load/', views.HWload, name='HWload'),
    path('HWChange/', views.HWChangeInfo, name='HWChangeInfo'),
    path('HWFixed/', views.HWFixedInfo, name='HWFixedInfo'),
    path('', views.index, name='index'),
]
