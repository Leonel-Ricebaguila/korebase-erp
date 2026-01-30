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
    """User registration view with OTP"""
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
            
            # Send Email
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
                # If email fails, delete user? Or just show error?
                # For safety, let's show error and allow retry logic (not implemented fully here)
                messages.error(request, f'Error enviando correo: {e}')
                # user.delete() # Optional cleanup
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
