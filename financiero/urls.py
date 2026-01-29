from django.urls import path
from . import views

app_name = 'financiero'

urlpatterns = [
    path('', views.index, name='index'),
]
