"""
Core URLs Configuration
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('logout/', views.logout_view, name='logout'),
    path('auth/google/', views.google_login_view, name='google_login'),
    path('auth/google/callback/', views.google_callback_view, name='google_callback'),
]
