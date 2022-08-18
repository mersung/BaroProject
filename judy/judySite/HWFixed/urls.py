from django.urls import path

from . import views

urlpatterns = [
    path('load/', views.load_refresh, name='HWload'),
    path('HWChange/', views.HWChangeInfo, name='HWChangeInfo'),
    path('HWFixed/', views.HWFixedInfo, name='HWFixedInfo'),
    path('', views.index, name='index'),
]
