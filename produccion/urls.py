from django.urls import path
from . import views

app_name = 'produccion'

urlpatterns = [
    # Dashboard
    path('', views.index, name='index'),

    # BOMs
    path('bom/', views.bom_list, name='bom_list'),
    path('bom/create/', views.bom_create, name='bom_create'),
    path('bom/<int:pk>/', views.bom_detail, name='bom_detail'),
    path('bom/<int:pk>/edit/', views.bom_edit, name='bom_edit'),

    # Work Orders
    path('orders/', views.workorder_list, name='workorder_list'),
    path('order/create/', views.workorder_create, name='workorder_create'),
    path('order/<int:pk>/', views.workorder_detail, name='workorder_detail'),
    path('order/<int:pk>/edit/', views.workorder_edit, name='workorder_edit'),
    path('order/<int:pk>/status/', views.workorder_status, name='workorder_status'),
]
