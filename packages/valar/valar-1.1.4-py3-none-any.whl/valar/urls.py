from django.urls import path

from .channels.views import handel_channel

urlpatterns = [
    path('socket/<str:handler>', handel_channel),
]
