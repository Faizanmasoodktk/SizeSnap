from django.urls import path
from . import views

urlpatterns = [
    path('resize', views.resize, name='resize')
]
