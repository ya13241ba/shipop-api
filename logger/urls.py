from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get-raw-log', views.getRawLog, name='index'),
    path('add-raw-log', views.addRawLog, name='index'),
]