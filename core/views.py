"""
Core Views - Authentication and Dashboard
KoreBase ERP System
"""
from django.contrib.auth import login, logout, authenticate
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.views import PasswordResetConfirmView
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


class KoreBasePasswordResetForm(PasswordResetForm):
    """
    Custom reset form that also allows accounts created via Google OAuth
    (which have no usable password) to receive a reset email and set
    a local password for the first time.
    """
    def get_users(self, email):
        """Return matching active users regardless of usable_password status."""
        active_users = CustomUser.objects.filter(
            email__iexact=email,
            is_active=True,
        )
        return active_users


class KoreBasePasswordResetConfirmView(PasswordResetConfirmView):
    """
    Custom confirm view that allows setting a password even when the
    original account had no usable password (OAuth-only accounts).
    """
    post_reset_login = True  # Auto-login after successful password set
    post_reset_login_backend = 'django.contrib.auth.backends.ModelBackend'
    success_url = '/core/'

    def form_valid(self, form):
        user = form.save()
        # Ensure account is activated and marked verified
        user.is_active = True
        user.email_verified = True
        user.save()
        return super().form_valid(form)



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
    """User logout view — clears all pending messages before logout
    to prevent previous session's notifications from leaking into the login page."""
    # Drain (consume) all unread messages so they don't bleed into the next session
    storage = get_messages(request)
    list(storage)  # Iterating through consumes and clears the message queue
    storage.used = True

    logout(request)
    # Add a single clean message AFTER logout (in the new anonymous session)
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


OAUTH_SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]


def _get_oauth_flow(redirect_uri):
    """
    Build Google OAuth flow from env vars (production) or JSON file (local dev).
    On Render the client_secret*.json file doesn't exist (gitignored),
    so we construct the config dict from GOOGLE_CLIENT_ID + GOOGLE_CLIENT_SECRET.
    """
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')

    if client_id and client_secret:
        # Production / env-var path — no JSON file needed
        client_config = {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            }
        }
        return Flow.from_client_config(
            client_config,
            scopes=OAUTH_SCOPES,
            redirect_uri=redirect_uri,
        )

    # Local dev fallback — use the JSON file
    client_secrets_path = os.getenv('GOOGLE_CLIENT_SECRETS_PATH')
    if client_secrets_path:
        return Flow.from_client_secrets_file(
            client_secrets_path,
            scopes=OAUTH_SCOPES,
            redirect_uri=redirect_uri,
        )

    raise ValueError("Google OAuth is not configured. Set GOOGLE_CLIENT_ID + GOOGLE_CLIENT_SECRET, or GOOGLE_CLIENT_SECRETS_PATH.")


def google_login_view(request):
    """
    Initiate Google OAuth2.0 flow
    Redirects user to Google's consent screen
    """
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    try:
        redirect_uri = request.build_absolute_uri('/core/auth/google/callback/')
        flow = _get_oauth_flow(redirect_uri)
        
        # Generate authorization URL
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        # Store state and code_verifier in session for the callback
        request.session['oauth_state'] = state
        request.session['oauth_code_verifier'] = flow.code_verifier
        
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
        
        redirect_uri = request.build_absolute_uri('/core/auth/google/callback/')
        flow = _get_oauth_flow(redirect_uri)
        
        # Restore PKCE code_verifier from login step
        code_verifier = request.session.pop('oauth_code_verifier', None)
        if code_verifier:
            flow.code_verifier = code_verifier
        
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
        
        # Get or create user — use filter().first() to avoid MultipleObjectsReturned
        user = CustomUser.objects.filter(email=email).first()
        created = False

        if user is None:
            # Generate unique username derived from the email prefix
            base_username = email.split('@')[0]
            username = base_username
            counter = 1
            while CustomUser.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            # Generate unique employee_id as well
            employee_id = base_username
            counter = 1
            while CustomUser.objects.filter(employee_id=employee_id).exists():
                employee_id = f"{base_username}{counter}"
                counter += 1

            user = CustomUser.objects.create(
                email=email,
                username=username,
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
            user.is_active = True  # Auto-activate if it was inactive (e.g. pending OTP)
            user.save()

        # IMPORTANT: specify backend so login() doesn't fail silently
        # when the user object wasn't returned by authenticate()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        if created:
            messages.success(request, f'Bienvenido, {user.get_full_name()}! Tu cuenta ha sido creada con Google.')
        else:
            messages.success(request, f'Bienvenido de nuevo, {user.get_full_name()}!')

        return redirect('core:dashboard')
        
    except Exception as e:
        messages.error(request, f'Error en autenticación con Google: {str(e)}')
        return redirect('core:login')

from django.db.models import Q
from logistica.models import Product, Warehouse, Supplier
from produccion.models import WorkOrder, BillOfMaterial
from financiero.models import Invoice

@login_required
def global_search_view(request):
    """HTMX endpoint for global autocomplete search"""
    query = request.GET.get('q', '').strip()
    if not query or len(query) < 2:
        return render(request, 'core/search_results.html', {'results': []})
    
    results = []
    
    # Busca Productos
    for p in Product.objects.filter(Q(sku__icontains=query) | Q(name__icontains=query))[:3]:
        results.append({'url': f"/logistica/inventory/", 'title': f"{p.sku} - {p.name}", 'type': 'Producto', 'icon': 'fa-box'})
        
    # Busca Almacenes
    for w in Warehouse.objects.filter(Q(code__icontains=query) | Q(name__icontains=query))[:3]:
        results.append({'url': f"/logistica/warehouses/", 'title': f"{w.code} - {w.name}", 'type': 'Almacén', 'icon': 'fa-warehouse'})
        
    # Busca Proveedores
    for s in Supplier.objects.filter(Q(code__icontains=query) | Q(name__icontains=query))[:3]:
        results.append({'url': f"/logistica/suppliers/", 'title': f"{s.code} - {s.name}", 'type': 'Proveedor', 'icon': 'fa-truck'})
        
    # Busca Ordenes de Trabajo
    for o in WorkOrder.objects.filter(work_order_number__icontains=query)[:3]:
        results.append({'url': f"/produccion/workorder/{o.pk}/", 'title': f"OT: {o.work_order_number}", 'type': 'Orden de Trabajo', 'icon': 'fa-clipboard-list'})
        
    # Busca Facturas
    for i in Invoice.objects.filter(invoice_number__icontains=query)[:3]:
        results.append({'url': f"/financiero/invoice/{i.pk}/", 'title': f"Factura: {i.invoice_number}", 'type': 'Factura', 'icon': 'fa-file-invoice-dollar'})
        
    return render(request, 'core/search_results.html', {'results': results})

@login_required
def notifications_list_view(request):
    """HTMX endpoint to render the notifications dropdown menu"""
    notifications = request.user.notifications.all()[:10]
    unread_count = request.user.notifications.filter(is_read=False).count()
    return render(request, 'core/notifications_dropdown.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })

@login_required
def mark_notification_read_view(request, pk):
    """HTMX endpoint to mark a single notification as read"""
    from .models import Notification
    try:
        notification = Notification.objects.get(pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
    except Notification.DoesNotExist:
        pass
        
    notifications = request.user.notifications.all()[:10]
    unread_count = request.user.notifications.filter(is_read=False).count()
    return render(request, 'core/notifications_dropdown.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })

@login_required
def notification_redirect_view(request, pk):
    """Marks a notification as read and redirects to its link"""
    from .models import Notification
    from django.shortcuts import get_object_or_404, redirect
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    
    if not notification.is_read:
        notification.is_read = True
        notification.save()
        
    if notification.link:
        return redirect(notification.link)
    return redirect('core:dashboard')

@login_required
def mark_all_notifications_read_view(request):
    """HTMX endpoint to mark all notifications as read"""
    request.user.notifications.filter(is_read=False).update(is_read=True)
    
    notifications = request.user.notifications.all()[:10]
    return render(request, 'core/notifications_dropdown.html', {
        'notifications': notifications,
        'unread_count': 0
    })
