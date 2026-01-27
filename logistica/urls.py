from django.urls import path
from . import views

app_name = 'logistica'

urlpatterns = [
    path('', views.index, name='index'),
    path('inventory/', views.inventory_list, name='inventory_list'),
]
