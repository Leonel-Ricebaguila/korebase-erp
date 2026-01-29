"""
Core Views - Authentication and Dashboard
KoreBase ERP System
"""
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages


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
