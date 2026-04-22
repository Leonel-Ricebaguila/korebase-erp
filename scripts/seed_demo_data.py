import os
import sys
import django
from decimal import Decimal

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "korebase.settings")
django.setup()

from django.contrib.auth.hashers import make_password
from core.models import CustomUser, Company
from logistica.models import Warehouse, Product, Stock, StockMovement
from django.utils import timezone

def seed_demo_data():
    print("[*] Iniciando creación de datos de demostración...")

    # 1. Crear Empresa
    company, created = Company.objects.get_or_create(
        name="TechNova Manufactura S.A. de C.V.",
        defaults={
            'rfc': 'TNM120101M2A',
            'is_trial': True,
            'trial_end_date': timezone.now() + timezone.timedelta(days=30)
        }
    )
    print(f"[*] Empresa: {company.name}")

    # 2. Crear Usuario Gerente
    user, u_created = CustomUser.objects.get_or_create(
        username="gerente_demo",
        defaults={
            'email': "gerente_demo@korebase.com",
            'first_name': "Gerente",
            'last_name': "Demo",
            'employee_id': "GER-001",
            'password': make_password('KoreBase2026!'),
            'is_active': True,
            'email_verified': True,
            'company': company
        }
    )
    if not u_created:
        user.password = make_password('KoreBase2026!')
        user.company = company
        user.save()
    print(f"[*] Usuario creado: {user.email} | Pass: KoreBase2026!")

    # 3. Crear Almacenes
    wh_main, _ = Warehouse.objects.get_or_create(
        company=company,
        code="ALM-001",
        defaults={'name': "Almacén Central (Materia Prima)", 'address': "Parque Industrial Norte"}
    )
    wh_prod, _ = Warehouse.objects.get_or_create(
        company=company,
        code="ALM-002",
        defaults={'name': "Centro de Distribución (Terminados)", 'address': "Bodega Sur"}
    )

    # 4. Crear Productos
    products_data = [
        {
            'sku': "MAT-MDR-01",
            'name': "Madera de Pino (Tablón)",
            'description': "Tablón de madera de pino tratada de 2x4",
            'category': "Materia Prima",
            'unit_cost': Decimal('150.00'),
            'clave_producto_sat': "11121600",
            'clave_unidad_sat': "XBX"
        },
        {
            'sku': "MAT-TRN-05",
            'name': "Tornillos de Acero 2 pulg",
            'description': "Caja con 100 tornillos de acero inoxidable",
            'category': "Materia Prima",
            'unit_cost': Decimal('45.50'),
            'clave_producto_sat': "31161500",
            'clave_unidad_sat': "H87"
        },
        {
            'sku': "PRD-MSA-01",
            'name': "Mesa de Comedor Rústica",
            'description': "Mesa de comedor para 6 personas acabado rústico",
            'category': "Producto Terminado",
            'unit_cost': Decimal('1200.00'),
            'clave_producto_sat': "56101500",
            'clave_unidad_sat': "H87"
        },
        {
            'sku': "MAT-PNT-02",
            'name': "Barniz Transparente 1L",
            'description': "Barniz de poliuretano acabado brillante",
            'category': "Materia Prima",
            'unit_cost': Decimal('180.00'),
            'clave_producto_sat': "31211500",
            'clave_unidad_sat': "LTR"
        }
    ]

    for p_data in products_data:
        prod, p_created = Product.objects.get_or_create(
            company=company,
            sku=p_data['sku'],
            defaults=p_data
        )
        
        # 5. Agregar Stock a cada producto
        if p_created:
            qty = Decimal('50.000') if prod.category == "Materia Prima" else Decimal('10.000')
            wh = wh_main if prod.category == "Materia Prima" else wh_prod
            
            stock, _ = Stock.objects.get_or_create(
                company=company,
                product=prod,
                warehouse=wh,
                defaults={'quantity': qty}
            )
            
            StockMovement.objects.create(
                company=company,
                product=prod,
                warehouse=wh,
                quantity_change=qty,
                movement_type='in',
                reference='Ajuste Inicial Demo',
                notes='Carga automática de demostración',
                user=user,
                unit_cost_at_movement=prod.unit_cost,
                running_balance=qty
            )

    print("[OK] Datos de demostración inyectados correctamente.")

if __name__ == "__main__":
    seed_demo_data()
