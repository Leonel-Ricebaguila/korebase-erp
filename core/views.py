"""
Core Views - Authentication and Dashboard
KoreBase ERP System
"""
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from .models import CustomUser, OTPToken
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
import secrets
import json
import os
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from google_auth_oauthlib.flow import Flow
from django.http import JsonResponse


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido, {user.get_full_name()}!')
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'core/login.html')


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente')
    return redirect('core:login')


@login_required
def dashboard_view(request):
    """Main dashboard view"""
    context = {
        'user': request.user,
        'total_users': 0,  # TODO: Get actual stats
    }
    return render(request, 'core/dashboard.html', context)


def register_view(request):
    """User registration view with OTP verification"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Inactive until OTP verification
            user.save()
            
            # Generate OTP
            otp_code = secrets.randbelow(1000000)
            otp_str = f"{otp_code:06d}"
            
            # Save OTP
            expires_at = timezone.now() + timedelta(minutes=10)
            OTPToken.objects.create(user=user, otp_code=otp_str, expires_at=expires_at)
            
            # Send Email (SendGrid in production, Gmail in development)
            try:
                send_mail(
                    'Código de Verificación - KoreBase',
                    f'Tu código de verificación es: {otp_str}\nExpira en 10 minutos.',
                    settings.DEFAULT_FROM_EMAIL or 'noreply@korebase.com',
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, f'Cuenta creada. Se ha enviado un código a {user.email}.')
                request.session['otp_user_id'] = user.id
                return redirect('core:verify_otp')
            except Exception as e:
                messages.error(request, f'Error enviando correo: {e}')
                user.delete()  # Cleanup failed registration
        else:
            messages.error(request, "Por favor corrige los errores señalados en el formulario.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'core/register.html', {'form': form})


def verify_otp_view(request):
    """Verify OTP Code"""
    user_id = request.session.get('otp_user_id')
    if not user_id:
        return redirect('core:login')
    
    if request.method == 'POST':
        otp_input = request.POST.get('otp_code')
        try:
            user = CustomUser.objects.get(id=user_id)
            # Find latest valid token
            token = OTPToken.objects.filter(
                user=user, 
                otp_code=otp_input,
                expires_at__gt=timezone.now()
            ).last()
            
            if token:
                user.is_active = True
                user.save()
                # Clear tokens
                user.otp_tokens.all().delete()
                
                login(request, user)
                del request.session['otp_user_id']
                messages.success(request, 'Cuenta verificada exitosamente.')
                return redirect('core:dashboard')
            else:
                messages.error(request, 'Código inválido o expirado.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
            return redirect('core:register')
            
    return render(request, 'core/verify_otp.html')


def google_login_view(request):
    """
    Initiate Google OAuth2.0 flow
    Redirects user to Google's consent screen
    """
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    try:
        # Get the path to client secrets from environment variable
        client_secrets_path = os.getenv('GOOGLE_CLIENT_SECRETS_PATH')
        
        if not client_secrets_path:
            messages.error(request, 'Configuración de Google OAuth no encontrada')
            return redirect('core:login')
        
        # Create OAuth flow
        flow = Flow.from_client_secrets_file(
            client_secrets_path,
            scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 
                   'https://www.googleapis.com/auth/userinfo.profile'],
            redirect_uri=request.build_absolute_uri('/core/auth/google/callback/')
        )
        
        # Generate authorization URL
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        # Store state in session for CSRF protection
        request.session['oauth_state'] = state
        
        return redirect(authorization_url)
        
    except Exception as e:
        messages.error(request, f'Error iniciando Google OAuth: {str(e)}')
        return redirect('core:login')


def google_callback_view(request):
    """
    Handle Google OAuth2.0 callback
    Process the authorization code and authenticate user
    """
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    try:
        # Verify state to prevent CSRF attacks
        state = request.GET.get('state')
        if not state or state != request.session.get('oauth_state'):
            messages.error(request, 'Error de seguridad: estado OAuth inválido')
            return redirect('core:login')
        
        # Clear the state from session
        del request.session['oauth_state']
        
        # Get the path to client secrets from environment variable
        client_secrets_path = os.getenv('GOOGLE_CLIENT_SECRETS_PATH')
        
        if not client_secrets_path:
            messages.error(request, 'Configuración de Google OAuth no encontrada')
            return redirect('core:login')
        
        # Create OAuth flow
        flow = Flow.from_client_secrets_file(
            client_secrets_path,
            scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email',
                   'https://www.googleapis.com/auth/userinfo.profile'],
            redirect_uri=request.build_absolute_uri('/core/auth/google/callback/')
        )
        
        # Exchange authorization code for credentials
        authorization_code = request.GET.get('code')
        if not authorization_code:
            messages.error(request, 'Código de autorización no proporcionado')
            return redirect('core:login')
        
        flow.fetch_token(code=authorization_code)
        credentials = flow.credentials
        
        # Get ID token and verify it
        id_info = id_token.verify_oauth2_token(
            credentials.id_token,
            google_requests.Request(),
            os.getenv('GOOGLE_CLIENT_ID')
        )
        
        # Extract user information
        email = id_info.get('email')
        name = id_info.get('name', '')
        given_name = id_info.get('given_name', '')
        family_name = id_info.get('family_name', '')
        
        if not email:
            messages.error(request, 'No se pudo obtener el correo electrónico de Google')
            return redirect('core:login')
        
        # Get or create user
        try:
            user = CustomUser.objects.get(email=email)
            created = False
        except CustomUser.DoesNotExist:
            # Generate unique employee_id
            base_employee_id = email.split('@')[0]
            employee_id = base_employee_id
            counter = 1
            
            # Ensure employee_id is unique
            while CustomUser.objects.filter(employee_id=employee_id).exists():
                employee_id = f"{base_employee_id}{counter}"
                counter += 1
            
            user = CustomUser.objects.create(
                email=email,
                username=base_employee_id,
                first_name=given_name,
                last_name=family_name,
                employee_id=employee_id,
                is_active=True,
                email_verified=True
            )
            created = True
        
        # Update user info if they already exist
        if not created:
            user.first_name = given_name
            user.last_name = family_name
            user.email_verified = True
            user.save()
        
        # Login the user
        login(request, user)
        
        if created:
            messages.success(request, f'Bienvenido, {user.get_full_name()}! Tu cuenta ha sido creada con Google.')
        else:
            messages.success(request, f'Bienvenido de nuevo, {user.get_full_name()}!')
        
        return redirect('core:dashboard')
        
    except Exception as e:
        messages.error(request, f'Error en autenticación con Google: {str(e)}')
        return redirect('core:login')
