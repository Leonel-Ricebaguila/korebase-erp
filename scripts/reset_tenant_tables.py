"""
Script para dropear las tablas antiguas y recrearlas con la nueva estructura Multi-Tenant.
SEGURO de ejecutar SOLO cuando la BD está vacía de datos de negocio.
"""
import sys
import os
sys.path.insert(0, r'c:\Users\jaque\OneDrive\Escritorio\Antigravity\Documents\UPY\DevSecOps\korebase-django')
os.environ['DJANGO_SETTINGS_MODULE'] = 'korebase.settings'
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_zMfniT4c7IjR@ep-red-cell-ahuue57k-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require'

import django
django.setup()

from django.db import connection

# Tables to drop in reverse dependency order (FK constraints)
tables_to_drop = [
    'financiero_journalentryline',
    'financiero_invoice',
    'financiero_journalentry',
    'financiero_chartofaccounts',
    'produccion_bomline',
    'produccion_workorder',
    'produccion_billofmaterial',
    'logistica_stockmovement',
    'logistica_stock',
    'logistica_product',
    'logistica_supplier',
    'logistica_warehouse',
]

with connection.cursor() as cursor:
    print("Dropping old tables...")
    for table in tables_to_drop:
        try:
            cursor.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE')
            print(f"  ✅ Dropped {table}")
        except Exception as e:
            print(f"  ❌ Error dropping {table}: {e}")
    
    # Reset django_migrations entries for these apps so migrate can recreate
    cursor.execute("""
        DELETE FROM django_migrations 
        WHERE app IN ('logistica', 'produccion', 'financiero')
    """)
    print(f"  ✅ Cleared migration history for logistica, produccion, financiero")

print("\nDone dropping. Now run: python manage.py migrate")
