#!/usr/bin/env python
import os
import sys
import django
import urllib.request
import bz2
import sqlite3
import tempfile
import time

# Configurar entorno de Django antes de llamar a base de datos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'korebase.settings')
django.setup()

from logistica.models import SatProductCode, SatUnitCode

URL_CATALOGO = "https://github.com/phpcfdi/resources-sat-catalogs/releases/latest/download/catalogs.db.bz2"

def main():
    print(f"[*] Iniciando migración de catálogos CFDI 4.0 desde el repositorio phpcfdi...")
    start_time = time.time()
    
    # 1. Rutas temporales limpias (Nunca alojadas en el repositorio para no hacer commits por accidente)
    bz2_path = os.path.join(tempfile.gettempdir(), "catalogs.db.bz2")
    db_path = os.path.join(tempfile.gettempdir(), "catalogs.db")
    
    print(f"[*] Descargando catálogo masivo desde GitHub ({URL_CATALOGO})...")
    # Utilizamos el módulo estándar para asegurar que corra nativo en Render y Local sin dependencias (ej. requests)
    urllib.request.urlretrieve(URL_CATALOGO, bz2_path)
    
    # 2. Descompresión BZ2 usando el módulo C integrado de Python (rapidísimo y nativo)
    print("[*] Descomprimiendo BZ2 a SQLite base local...")
    with bz2.BZ2File(bz2_path, 'rb') as source, open(db_path, 'wb') as dest:
        for data in iter(lambda: source.read(100 * 1024), b''):
            dest.write(data)
            
    # 3. Tratamiento de Datos
    print("[*] Conectando a la DB extraída y parseando tablas originales...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # A) PRODUCTOS
        # En el esquema SQLite phpcfdi la tabla es cfdi_40_productos_servicios (id, texto)
        cursor.execute("SELECT id, texto FROM cfdi_40_productos_servicios")
        rows_prod = cursor.fetchall()
        
        print(f"[*] Leyendo y transformando {len(rows_prod)} claves de productos/servicios SAT...")
        product_objs = [
            SatProductCode(code=row[0], description=row[1]) for row in rows_prod
        ]
            
        print("[*] Inyectando productos a la base de datos de Django (bulk_create de 5,000 llaves)...")
        # El ignore_conflicts ignora si hay duplicados (nuestra llave es unique) logrando la máxima velocidad O(1)
        SatProductCode.objects.bulk_create(product_objs, batch_size=5000, ignore_conflicts=True)
        
        # B) UNIDADES
        cursor.execute("SELECT id, texto FROM cfdi_40_claves_unidades")
        rows_unidades = cursor.fetchall()
        
        print(f"[*] Leyendo y transformando {len(rows_unidades)} claves de unidad métrica SAT...")
        unit_objs = [
            SatUnitCode(code=row[0], name=row[1]) for row in rows_unidades
        ]
            
        print("[*] Inyectando unidades a la base de datos de Django...")
        SatUnitCode.objects.bulk_create(unit_objs, batch_size=2000, ignore_conflicts=True)
        
    except sqlite3.OperationalError as db_err:
        print(f"[!] Error leyendo la DB de phpcfdi: Es posible que los nombres de tablas cambiaran. Detalles: {db_err}")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        print(f"Tablas disponibles: {cursor.fetchall()}")
    except Exception as e:
        print(f"[!] Error critico durante la inyeccion SQL: {e}")
    finally:
        conn.close()
        
    # 4. Cleanup Automatico
    print("[*] Limpiando y borrando archivos temporales...")
    if os.path.exists(bz2_path): os.remove(bz2_path)
    if os.path.exists(db_path): os.remove(db_path)
    
    end_time = time.time()
    
    # 5. Reporte de Finalizacion
    print("\n==================================")
    print(f"[OK] Operacion CFDI 4.0 Completada! ({end_time - start_time:.2f} seg)")
    print(f"     Productos Vigentes en DB: {SatProductCode.objects.count()}")
    print(f"     Unidades  Vigentes en DB: {SatUnitCode.objects.count()}")
    print("==================================\n")

if __name__ == '__main__':
    main()
