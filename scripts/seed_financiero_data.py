import os
import sys
import django
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "korebase.settings")
django.setup()

from core.models import CustomUser, Company
from financiero.models import ChartOfAccounts, JournalEntry, JournalEntryLine, Invoice

def seed_financiero_data():
    print("[*] Iniciando creación de datos financieros...")
    
    # Get the existing demo company and user
    company = Company.objects.filter(name="TechNova Manufactura S.A. de C.V.").first()
    if not company:
        print("[!] No se encontró la empresa demo. Ejecuta seed_demo_data primero.")
        return
        
    user = CustomUser.objects.filter(username="gerente_demo").first()
    if not user:
        print("[!] No se encontró el usuario demo.")
        return

    # 1. Crear Plan de Cuentas (Chart of Accounts)
    acc_caja, _ = ChartOfAccounts.objects.get_or_create(company=company, account_code='1010', defaults={'account_name': 'Caja General', 'account_type': 'asset'})
    acc_bancos, _ = ChartOfAccounts.objects.get_or_create(company=company, account_code='1020', defaults={'account_name': 'Bancos Nacionales', 'account_type': 'asset'})
    acc_inventario, _ = ChartOfAccounts.objects.get_or_create(company=company, account_code='1140', defaults={'account_name': 'Inventario de Materias Primas', 'account_type': 'asset'})
    acc_proveedores, _ = ChartOfAccounts.objects.get_or_create(company=company, account_code='2010', defaults={'account_name': 'Proveedores Nacionales', 'account_type': 'liability'})
    acc_capital, _ = ChartOfAccounts.objects.get_or_create(company=company, account_code='3010', defaults={'account_name': 'Capital Social', 'account_type': 'equity'})
    acc_ventas, _ = ChartOfAccounts.objects.get_or_create(company=company, account_code='4010', defaults={'account_name': 'Ventas Netas', 'account_type': 'income'})
    acc_costo_ventas, _ = ChartOfAccounts.objects.get_or_create(company=company, account_code='5010', defaults={'account_name': 'Costo de Ventas', 'account_type': 'expense'})

    # 2. Asiento de Apertura (Initial Investment)
    if not JournalEntry.objects.filter(company=company, entry_number='AS-0001').exists():
        entry1 = JournalEntry.objects.create(
            company=company,
            entry_number='AS-0001',
            entry_date=timezone.now().date() - timedelta(days=5),
            description='Apertura de Capital Social (Aportación Inicial)',
            created_by=user
        )
        JournalEntryLine.objects.create(journal_entry=entry1, account=acc_bancos, debit=Decimal('500000.00'), credit=Decimal('0.00'), description='Aportación Socios')
        JournalEntryLine.objects.create(journal_entry=entry1, account=acc_capital, debit=Decimal('0.00'), credit=Decimal('500000.00'), description='Aportación Socios')

    # 3. Compra de Inventario a Proveedor
    if not JournalEntry.objects.filter(company=company, entry_number='AS-0002').exists():
        entry2 = JournalEntry.objects.create(
            company=company,
            entry_number='AS-0002',
            entry_date=timezone.now().date() - timedelta(days=2),
            description='Compra de Materia Prima Inicial',
            created_by=user
        )
        JournalEntryLine.objects.create(journal_entry=entry2, account=acc_inventario, debit=Decimal('150000.00'), credit=Decimal('0.00'), description='Entrada a almacén')
        JournalEntryLine.objects.create(journal_entry=entry2, account=acc_proveedores, debit=Decimal('0.00'), credit=Decimal('150000.00'), description='Deuda a Maderería El Pino')

    # 4. Crear Facturas (Invoices) - Gastos e Ingresos
    if not Invoice.objects.filter(company=company, invoice_number='FAC-P-101').exists():
        Invoice.objects.create(
            company=company,
            invoice_number='FAC-P-101',
            invoice_type='supplier',
            status='paid',
            customer_supplier='Maderería El Pino S.A. de C.V.',
            invoice_date=timezone.now().date() - timedelta(days=2),
            due_date=timezone.now().date() + timedelta(days=28),
            subtotal=Decimal('129310.34'),
            tax_amount=Decimal('20689.66'),
            total=Decimal('150000.00'),
            created_by=user
        )
        
    if not Invoice.objects.filter(company=company, invoice_number='FAC-C-001').exists():
        Invoice.objects.create(
            company=company,
            invoice_number='FAC-C-001',
            invoice_type='customer',
            status='issued',
            customer_supplier='Mueblerías Nacionales S.A.',
            invoice_date=timezone.now().date() - timedelta(days=1),
            due_date=timezone.now().date() + timedelta(days=14),
            subtotal=Decimal('45000.00'),
            tax_amount=Decimal('7200.00'),
            total=Decimal('52200.00'),
            created_by=user
        )
        
    if not Invoice.objects.filter(company=company, invoice_number='FAC-C-002').exists():
        Invoice.objects.create(
            company=company,
            invoice_number='FAC-C-002',
            invoice_type='customer',
            status='paid',
            customer_supplier='Hotel Resort Paraíso',
            invoice_date=timezone.now().date(),
            due_date=timezone.now().date(),
            subtotal=Decimal('80000.00'),
            tax_amount=Decimal('12800.00'),
            total=Decimal('92800.00'),
            created_by=user
        )

    print("[OK] Datos financieros (Cuentas, Asientos, Facturas) inyectados correctamente.")

if __name__ == "__main__":
    seed_financiero_data()
