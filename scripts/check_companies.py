import sys, os
sys.path.insert(0, r'c:\Users\jaque\OneDrive\Escritorio\Antigravity\Documents\UPY\DevSecOps\korebase-django')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'korebase.settings')
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_zMfniT4c7IjR@ep-red-cell-ahuue57k-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require'
import django; django.setup()

from core.models import CustomUser, Company

u = CustomUser.objects.filter(email__icontains='kikes').first()
print(f'User: {u.email}')
print(f'Company Name: {u.company.name}')
print(f'Company UUID: {u.company_id}')
print(f'Trial: {u.company.is_trial}')
print(f'Trial ends: {u.company.trial_end_date.strftime("%Y-%m-%d")}')
print(f'Subscription: {u.company.subscription_tier}')
print()
print('All companies:')
for c in Company.objects.all():
    users = CustomUser.objects.filter(company=c).values_list('email', flat=True)
    print(f'  UUID: {c.id}')
    print(f'  Name: {c.name}')
    print(f'  Users: {list(users)}')
    print()
