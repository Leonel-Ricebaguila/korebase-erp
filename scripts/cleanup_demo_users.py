import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'korebase.settings')
django.setup()

from logistica.models import StockMovement, Product, Warehouse, Supplier
from produccion.models import WorkOrder, BillOfMaterial, BOMLine 
from financiero.models import Invoice
from core.models import CustomUser, Company, Notification, OTPToken

def run_cleanup():
    print("[*] Blank slate: Preparando base de datos para la Demostración...")

    admin_user = CustomUser.objects.filter(username='admin').first()
    if not admin_user:
        print("[!] No se encontró al admin. Abortando.")
        return

    print("[*] Borrando TODA la data operativa para evitar candados (Se preserva el Catálogo SAT)...")
    StockMovement.objects.all().delete()
    BOMLine.objects.all().delete()
    BillOfMaterial.objects.all().delete()
    WorkOrder.objects.all().delete()
    Invoice.objects.all().delete()
    
    print("[*] Borrando catálogos secundarios...")
    Product.objects.all().delete()
    Warehouse.objects.all().delete()
    Supplier.objects.all().delete()

    print("[*] Borrando notificaciones y tokens de seguridad...")
    Notification.objects.all().delete()
    OTPToken.objects.all().delete()

    print("[*] Eliminando todos los usuarios excepto 'admin'...")
    CustomUser.objects.exclude(id=admin_user.id).delete()

    print("[*] Eliminando todas las empresas, excepto la del 'admin'...")
    Company.objects.exclude(id=admin_user.company_id).delete()

    print("[OK] Tabula Rasa. Tu Base de Datos ahora está limpia como un quirófano.")

if __name__ == '__main__':
    run_cleanup()
