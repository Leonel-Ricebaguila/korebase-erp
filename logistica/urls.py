from django.urls import path
from . import views

app_name = 'logistica'

urlpatterns = [
    # Dashboard
    path('', views.index, name='index'),
    
    # Inventory
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('product/create/', views.product_create, name='product_create'),
    path('product/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # Warehouses
    path('warehouse/create/', views.warehouse_create, name='warehouse_create'),
    path('warehouse/<int:pk>/edit/', views.warehouse_edit, name='warehouse_edit'),
    path('warehouse/<int:pk>/delete/', views.warehouse_delete, name='warehouse_delete'),
    
    # Suppliers
    path('supplier/create/', views.supplier_create, name='supplier_create'),
    path('supplier/<int:pk>/edit/', views.supplier_edit, name='supplier_edit'),
    path('supplier/<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),
]
