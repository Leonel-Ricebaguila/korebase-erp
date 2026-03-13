import sys, os
sys.path.insert(0, r'c:\Users\jaque\OneDrive\Escritorio\Antigravity\Documents\UPY\DevSecOps\korebase-django')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'korebase.settings')
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_zMfniT4c7IjR@ep-red-cell-ahuue57k-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require'
import django; django.setup()

from django.db import connection

with connection.cursor() as cursor:
    # Report what we're about to delete
    cursor.execute("SELECT id, code, name FROM logistica_warehouse WHERE company_id IS NULL")
    orphans = cursor.fetchall()
    print(f'Orphan warehouses: {orphans}')
    
    # Delete child records first (FK pointing to orphan warehouse)
    cursor.execute("""
        DELETE FROM logistica_stockmovement 
        WHERE warehouse_id IN (
            SELECT id FROM logistica_warehouse WHERE company_id IS NULL
        )
    """)
    print(f'  Deleted {cursor.rowcount} orphan StockMovements')
    
    cursor.execute("""
        DELETE FROM logistica_stock 
        WHERE warehouse_id IN (
            SELECT id FROM logistica_warehouse WHERE company_id IS NULL
        )
    """)
    print(f'  Deleted {cursor.rowcount} orphan Stocks')
    
    # Now delete orphan warehouses
    cursor.execute("DELETE FROM logistica_warehouse WHERE company_id IS NULL")
    print(f'  Deleted {cursor.rowcount} orphan Warehouses')

    # Delete orphan products without company
    cursor.execute("DELETE FROM logistica_product WHERE company_id IS NULL")
    print(f'  Deleted {cursor.rowcount} orphan Products')
    
    cursor.execute("DELETE FROM logistica_supplier WHERE company_id IS NULL")
    print(f'  Deleted {cursor.rowcount} orphan Suppliers')

print('\n✅ All orphans cleaned.')
