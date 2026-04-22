"""
Core URLs Configuration
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import KoreBasePasswordResetForm, KoreBasePasswordResetConfirmView

app_name = 'core'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('logout/', views.logout_view, name='logout'),
    path('auth/google/', views.google_login_view, name='google_login'),
    path('auth/google/callback/', views.google_callback_view, name='google_callback'),
    path('search/', views.global_search_view, name='global_search'),
    path('settings/', views.settings_view, name='settings'),
    path('invite/', views.invite_member_view, name='invite_member'),
    path('join/<uuid:token>/', views.join_company_view, name='join_company'),
    path('invitations/', views.invitations_list_view, name='invitations_list'),

    # Notifications
    path('notifications/', views.notifications_list_view, name='notifications_list'),
    path('notifications/<int:pk>/read/', views.mark_notification_read_view, name='mark_notification_read'),
    path('notifications/<int:pk>/redirect/', views.notification_redirect_view, name='notification_redirect'),
    path('notifications/read-all/', views.mark_all_notifications_read_view, name='mark_all_notifications_read'),

    # Password reset — custom views to support OAuth-only accounts
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html',
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt',
             form_class=KoreBasePasswordResetForm,  # Allows OAuth accounts
             success_url='/core/password-reset/done/',
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html',
         ),
         name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/',
         KoreBasePasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html',
         ),
         name='password_reset_complete'),
]
