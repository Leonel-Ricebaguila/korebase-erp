import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'korebase.settings')
django.setup()

from django.db import connection

def run_cleanup():
    print("[*] Blank slate: Ejecutando borrado bruto en SQL...")

    with connection.cursor() as cursor:
        print("[*] Truncando datos operativos...")
        cursor.execute("DELETE FROM logistica_stock;")
        cursor.execute("DELETE FROM logistica_stockmovement;")
        cursor.execute("DELETE FROM produccion_bomline;")
        cursor.execute("DELETE FROM produccion_billofmaterial;")
        cursor.execute("DELETE FROM produccion_workorder;")
        cursor.execute("DELETE FROM financiero_invoice;")
        cursor.execute("DELETE FROM logistica_product;")
        cursor.execute("DELETE FROM logistica_supplier;")
        cursor.execute("DELETE FROM logistica_warehouse;")
        
        print("[*] Borrando notificaciones temporales...")
        cursor.execute("DELETE FROM core_notification;")
        cursor.execute("DELETE FROM core_otptoken;")
        
        print("[*] Borrando usuarios fantasma...")
        cursor.execute("DELETE FROM core_customuser_groups WHERE customuser_id IN (SELECT id FROM core_customuser WHERE username != 'admin');")
        cursor.execute("DELETE FROM core_customuser_user_permissions WHERE customuser_id IN (SELECT id FROM core_customuser WHERE username != 'admin');")
        cursor.execute("DELETE FROM core_customuser WHERE username != 'admin';")
        
        print("[*] Borrando Empresas fantasma...")
        cursor.execute("DELETE FROM core_company WHERE name NOT ILIKE '%admin%';")

    print("[OK] Tabula Rasa completada con éxito.")

if __name__ == '__main__':
    run_cleanup()
