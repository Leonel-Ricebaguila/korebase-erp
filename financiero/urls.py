from django.urls import path
from . import views

app_name = 'financiero'

urlpatterns = [
    # Dashboard
    path('', views.index, name='index'),

    # Chart of Accounts
    path('accounts/', views.accounts_list, name='accounts_list'),
    path('account/create/', views.account_create, name='account_create'),
    path('account/<int:pk>/edit/', views.account_edit, name='account_edit'),

    # Journal Entries
    path('journal/', views.journal_list, name='journal_list'),
    path('journal/create/', views.journal_create, name='journal_create'),
    path('journal/<int:pk>/', views.journal_detail, name='journal_detail'),
    path('journal/<int:pk>/reverse/', views.journal_reverse, name='journal_reverse'),

    # Invoices
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoice/create/', views.invoice_create, name='invoice_create'),
    path('invoice/<int:pk>/edit/', views.invoice_edit, name='invoice_edit'),
    path('invoice/<int:pk>/status/', views.invoice_status, name='invoice_status'),
]
