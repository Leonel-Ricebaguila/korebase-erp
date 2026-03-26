import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'korebase.settings')
django.setup()

from logistica.models import SatProductCode, SatUnitCode

# Catálogo pre-cargado de muestra para UX/MX
COMMON_SAT_PRODUCTS = [
    {"code": "50112000", "description": "Carnes procesadas y preparadas"},
    {"code": "50111500", "description": "Carne y aves de corral frescas"},
    {"code": "50202300", "description": "Bebidas no alcohólicas (Agua, Jugos)"},
    {"code": "50202301", "description": "Agua potable"},
    {"code": "43211500", "description": "Computadores corporativos"},
    {"code": "43211503", "description": "Computadores portátiles (Laptops)"},
    {"code": "81111500", "description": "Servicios de ingeniería de software"},
    {"code": "80111617", "description": "Servicios de arquitectura y construcción"},
    {"code": "85121600", "description": "Servicios de doctores especialistas"},
    {"code": "72101500", "description": "Servicios de apoyo a la construcción"},
    {"code": "44122100", "description": "Sujetadores de papel (Clips, grapas)"},
    {"code": "14111500", "description": "Papel de impresión y escritura"},
]

COMMON_SAT_UNITS = [
    {"code": "H87", "name": "Pieza"},
    {"code": "E48", "name": "Unidad de servicio"},
    {"code": "KGM", "name": "Kilogramo"},
    {"code": "LTR", "name": "Litro"},
    {"code": "MTR", "name": "Metro"},
    {"code": "PR",  "name": "Par"},
    {"code": "XBX", "name": "Caja"},
    {"code": "XPK", "name": "Paquete"},
    {"code": "DAY", "name": "Día"},
    {"code": "HUR", "name": "Hora"},
]

def seed_data():
    print("Iniciando inyección del catálogo SAT...")
    
    products_created = 0
    for prod in COMMON_SAT_PRODUCTS:
        obj, created = SatProductCode.objects.get_or_create(
            code=prod['code'],
            defaults={'description': prod['description']}
        )
        if created:
            products_created += 1

    units_created = 0
    for unit in COMMON_SAT_UNITS:
        obj, created = SatUnitCode.objects.get_or_create(
            code=unit['code'],
            defaults={'name': unit['name']}
        )
        if created:
            units_created += 1

    print(f"Éxito! Se añadieron {products_created} claves de productos y {units_created} claves de unidad.")
    print(f"Total en DB: {SatProductCode.objects.count()} Productos, {SatUnitCode.objects.count()} Unidades.")

if __name__ == '__main__':
    seed_data()
