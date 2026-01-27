#!/bin/bash
# Script para iniciar KoreBase ERP en modo desarrollo

cd /home/nico/Desktop/Programación/DEVSECOPS/korebase-django

echo "🚀 Iniciando KoreBase ERP..."
echo ""

# Activar virtual environment
source venv/bin/activate

# Aplicar migraciones pendientes
echo "📦 Aplicando migraciones..."
python manage.py migrate

echo ""
echo "✨ Iniciando servidor de desarrollo..."
echo "📍 URL: http://localhost:8000"
echo "👤 Usuario: admin"
echo "🔑 Contraseña: admin123"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

# Iniciar servidor
python manage.py runserver 0.0.0.0:8000
