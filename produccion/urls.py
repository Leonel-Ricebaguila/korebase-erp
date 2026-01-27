from django.urls import path
from . import views

app_name = 'produccion'

urlpatterns = [
    path('', views.index, name='index'),
]
