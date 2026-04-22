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
from django.utils import timezone
from .models import Company


def _ensure_company(user, invitation_token=None):
    """
    Multi-Tenant: Asigna una Empresa al usuario y crea su CompanyMembership.

    Flujo con invitación:
      Si se provee un invitation_token válido (CompanyInvitation), el usuario
      se une a la empresa de la invitación con el rol especificado en ella.
      NO se crea empresa nueva. La invitación se marca como 'accepted'.

    Flujo sin invitación (registro normal):
      Se crea una nueva Empresa de prueba (15 días) y el usuario recibe
      automáticamente el rol 'owner' de esa empresa.
    """
    from .models import CompanyMembership, CompanyInvitation

    if invitation_token:
        # --- FLUJO INVITADO ---
        try:
            invitation = CompanyInvitation.objects.get(token=invitation_token)
            if not invitation.is_valid:
                # Token expirado o ya usado — fallback a crear empresa propia
                pass
            else:
                company = invitation.company
                user.company = company
                user.save(update_fields=['company'])

                # Crear membresía con el rol de la invitación
                CompanyMembership.objects.get_or_create(
                    user=user,
                    company=company,
                    defaults={'role': invitation.role}
                )

                # Sellar la invitación — no reutilizable
                invitation.status = 'accepted'
                invitation.accepted_by = user
                invitation.accepted_at = timezone.now()
                invitation.save(update_fields=['status', 'accepted_by', 'accepted_at'])

                return company
        except CompanyInvitation.DoesNotExist:
            pass  # Si el token no existe, caemos al flujo normal abajo

    # --- FLUJO NORMAL: crear empresa propia como owner ---
    if user.company is None:
        company = Company.objects.create(
            name=f"Empresa de {user.get_full_name() or user.username}",
            is_trial=True,
            trial_end_date=timezone.now() + timezone.timedelta(days=15),
        )
        user.company = company
        user.save(update_fields=['company'])

        # El creador siempre es 'owner'
        CompanyMembership.objects.get_or_create(
            user=user,
            company=company,
            defaults={'role': 'owner'}
        )

    return user.company


def get_user_membership(user):
    """Retorna el CompanyMembership activo del usuario en su empresa actual."""
    from .models import CompanyMembership
    if user.company is None:
        return None
    return CompanyMembership.objects.filter(user=user, company=user.company).first()


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
    """Main dashboard view with REAL data"""
    company = request.user.company
    from logistica.models import Stock
    from produccion.models import WorkOrder
    from django.db.models import Sum, F
    from decimal import Decimal
    
    # Logistica KPIs
    raw_val = Stock.objects.filter(company=company, product__category='Materia Prima').annotate(
        value=F('quantity') * F('product__unit_cost')
    ).aggregate(t=Sum('value'))['t'] or Decimal('0.00')
    
    fin_val = Stock.objects.filter(company=company, product__category='Producto Terminado').annotate(
        value=F('quantity') * F('product__unit_cost')
    ).aggregate(t=Sum('value'))['t'] or Decimal('0.00')
    
    # Produccion KPIs
    active_orders = WorkOrder.objects.filter(company=company, status__in=['pending', 'in_progress']).count()
    
    context = {
        'user': request.user,
        'active_orders': active_orders,
        'raw_material_val': float(raw_val),
        'finished_goods_val': float(fin_val),
        'other_stock_val': 0.0,
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
                # OVERRIDE FOR DEMO: If SendGrid API fails, don't delete user. Just log the OTP to Render Logs!
                print(f"==================================================")
                print(f"[!] SMTP API (SendGrid) FALLÓ con error: {e}")
                print(f"[*] BYPASS DE EMERGENCIA PARA DEMO.")
                print(f"[*] EL CÓDIGO OTP PARA {user.email} ES: >>> {otp_str} <<<")
                print(f"==================================================")
                
                messages.warning(request, f'El servidor de correos está saturado. Revisa la consola de Render para ver tu código OTP (Modo Desarrollador).')
                request.session['otp_user_id'] = user.id
                return redirect('core:verify_otp')
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

                # Multi-Tenant: Asignar empresa (propia o vía invitación)
                invitation_token = request.session.pop('pending_invitation_token', None)
                _ensure_company(user, invitation_token=invitation_token)

                login(request, user)
                del request.session['otp_user_id']
                messages.success(request, '¡Cuenta verificada exitosamente. Bienvenido a KoreBase!')
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
            # Multi-Tenant: Asignar empresa (propia o vía invitación en sesión)
            invitation_token = request.session.pop('pending_invitation_token', None)
            _ensure_company(user, invitation_token=invitation_token)
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

@login_required
def settings_view(request):
    """View and update company settings (Early Access mode). Uses current user's Company."""
    company = request.user.company
    from .forms import CompanyProfileForm
    from logistica.models import Warehouse

    if request.method == 'POST':
        # Simple processing for Company profile
        if 'update_profile' in request.POST:
            form = CompanyProfileForm(request.POST, request.FILES, instance=company)
            if form.is_valid():
                form.save()
                messages.success(request, "Perfil de la empresa actualizado correctamente.")
                return redirect('core:settings')
            else:
                messages.error(request, "Hubo un error actualizando el perfil.")
    else:
        form = CompanyProfileForm(instance=company)

    # Active warehouses for the Company
    warehouses = Warehouse.objects.filter(company=company)

    # Team members and their memberships
    from .models import CompanyMembership
    memberships = CompanyMembership.objects.filter(company=company).select_related('user')

    context = {
        'company': company,
        'form': form,
        'warehouses': warehouses,
        'memberships': memberships,
        'user_membership': get_user_membership(request.user),
        'title': 'Configuración'
    }
    return render(request, 'core/settings.html', context)


# ==================== INVITACIONES ====================

@login_required
def invite_member_view(request):
    """
    Genera una invitación de empresa y envía el link al correo del invitado.
    Solo accesible para usuarios con rol owner o admin.
    """
    from .forms import InviteMemberForm
    from .models import CompanyInvitation, CompanyMembership
    from datetime import timedelta

    membership = get_user_membership(request.user)
    if not membership or not membership.can_invite:
        messages.error(request, "No tienes permisos para invitar usuarios.")
        return redirect('core:settings')

    if request.method == 'POST':
        form = InviteMemberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            role  = form.cleaned_data['role']

            # OPCIÓN A — Aislamiento Estricto: el email no puede tener cuenta existente
            existing_user = CustomUser.objects.filter(email__iexact=email).first()
            if existing_user:
                if existing_user.company == request.user.company:
                    messages.warning(request, f"{email} ya es miembro de esta empresa.")
                else:
                    messages.error(
                        request,
                        f"El correo {email} ya tiene una cuenta en KoreBase asociada a otra empresa. "
                        "Por política de seguridad (Aislamiento Estricto), no puede unirse a esta empresa. "
                        "Pide al usuario que use un correo corporativo diferente."
                    )
                return redirect('core:invite_member')

            # Verificar que no haya ya una invitación pendiente para este email
            existing_invite = CompanyInvitation.objects.filter(
                company=request.user.company,
                email__iexact=email,
                status='pending'
            ).first()
            if existing_invite and existing_invite.is_valid:
                messages.warning(request, f"Ya existe una invitación pendiente para {email}.")
                return redirect('core:invitations_list')

            # Crear la invitación con 48h de vigencia
            invitation = CompanyInvitation.objects.create(
                company=request.user.company,
                invited_by=request.user,
                email=email,
                role=role,
                expires_at=timezone.now() + timedelta(hours=48),
            )

            # Construir el enlace de unión
            join_url = request.build_absolute_uri(f'/core/join/{invitation.token}/')

            # Enviar correo con el enlace
            # NOTA: Usamos EMAIL_HOST_USER como remitente verificado en SendGrid.
            # 'noreply@korebase.com' NO está verificado en SendGrid y causa rechazo silencioso.
            import os as _os
            verified_sender = (
                _os.getenv('EMAIL_HOST_USER')  # e.g. sistema.autenticacion.ica@gmail.com
                or settings.DEFAULT_FROM_EMAIL
            )
            try:
                send_mail(
                    subject=f'Invitación a {request.user.company.name} en KoreBase',
                    message=(
                        f"Hola,\n\n"
                        f"{request.user.get_full_name()} te ha invitado a unirte a "
                        f"{request.user.company.name} en KoreBase ERP como {invitation.get_role_display()}.\n\n"
                        f"Acepta la invitación aquí (válida por 48 horas):\n{join_url}\n\n"
                        f"Si no esperabas este correo, puedes ignorarlo.\n\n"
                        f"— El equipo de KoreBase"
                    ),
                    from_email=verified_sender,
                    recipient_list=[email],
                    fail_silently=False,
                )
                messages.success(request, f"Invitación enviada exitosamente a {email}.")
            except Exception as e:
                # No fallar si el correo falla — la invitación ya existe y el enlace es visible en la lista
                print(f"[!] Email de invitación falló para {email}: {e}")
                messages.warning(
                    request,
                    f"Invitación creada, pero el correo no pudo enviarse a {email}. "
                    f"Ve a 'Historial de Invitaciones' para copiar y compartir el enlace manualmente."
                )

            return redirect('core:invitations_list')
    else:
        form = InviteMemberForm()

    return render(request, 'core/invite_member.html', {
        'form': form,
        'company': request.user.company,
        'title': 'Invitar Colaborador'
    })


def join_company_view(request, token):
    """
    Procesa el enlace de invitación (/core/join/<uuid>/).
    - Si el usuario ya está logueado y su email coincide: acepta directamente.
    - Si no está logueado: guarda el token en sesión y redirige al registro.
    - Si el token es inválido o expirado: muestra página de error amigable.
    """
    from .models import CompanyInvitation, CompanyMembership

    try:
        invitation = CompanyInvitation.objects.select_related('company').get(token=token)
    except CompanyInvitation.DoesNotExist:
        return render(request, 'core/join_error.html', {
            'reason': 'not_found',
            'title': 'Invitación no encontrada'
        })

    if not invitation.is_valid:
        return render(request, 'core/join_error.html', {
            'reason': 'expired' if invitation.status == 'pending' else invitation.status,
            'title': 'Invitación inválida'
        })

    # Si el usuario YA está autenticado
    if request.user.is_authenticated:
        if request.user.email.lower() != invitation.email.lower():
            return render(request, 'core/join_error.html', {
                'reason': 'wrong_email',
                'invitation': invitation,
                'title': 'Correo no coincide'
            })

        # Email coincide → aceptar directamente
        request.user.company = invitation.company
        request.user.save(update_fields=['company'])

        CompanyMembership.objects.get_or_create(
            user=request.user,
            company=invitation.company,
            defaults={'role': invitation.role}
        )

        invitation.status = 'accepted'
        invitation.accepted_by = request.user
        invitation.accepted_at = timezone.now()
        invitation.save(update_fields=['status', 'accepted_by', 'accepted_at'])

        messages.success(
            request,
            f'¡Te has unido a {invitation.company.name} como {invitation.get_role_display()}!'
        )
        return redirect('core:dashboard')

    # No está autenticado → guardar token en sesión y redirigir al registro
    request.session['pending_invitation_token'] = str(token)
    request.session['invitation_company_name'] = invitation.company.name
    request.session['invitation_email'] = invitation.email
    messages.info(
        request,
        f'Estás siendo invitado a unirte a {invitation.company.name}. '
        'Crea tu cuenta o inicia sesión para aceptar.'
    )
    return redirect('core:register')


@login_required
def invitations_list_view(request):
    """Lista las invitaciones enviadas por la empresa del usuario y permite revocarlas."""
    from .models import CompanyInvitation

    membership = get_user_membership(request.user)
    if not membership or not membership.can_invite:
        messages.error(request, "No tienes permisos para ver las invitaciones.")
        return redirect('core:settings')

    if request.method == 'POST':
        # Revocar una invitación
        invite_id = request.POST.get('revoke_id')
        if invite_id:
            try:
                inv = CompanyInvitation.objects.get(
                    pk=invite_id,
                    company=request.user.company,
                    status='pending'
                )
                inv.status = 'revoked'
                inv.save(update_fields=['status'])
                messages.success(request, "Invitación revocada.")
            except CompanyInvitation.DoesNotExist:
                messages.error(request, "Invitación no encontrada o ya procesada.")
        return redirect('core:invitations_list')

    invitations = CompanyInvitation.objects.filter(
        company=request.user.company
    ).select_related('invited_by', 'accepted_by').order_by('-created_at')

    return render(request, 'core/invitations_list.html', {
        'invitations': invitations,
        'company': request.user.company,
        'title': 'Invitaciones Enviadas'
    })

