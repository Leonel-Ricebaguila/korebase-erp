import sys
content = open(r'c:\Users\jaque\OneDrive\Escritorio\Antigravity\Documents\UPY\DevSecOps\korebase-django\produccion\forms.py', 'r', encoding='utf-8').read()
# Find the start of the old duplicate class that begins without the Tenant-aware comment
marker = '\nclass BillOfMaterialForm(forms.ModelForm):\n    """Form for creating/editing BOMs"""'
idx = content.find(marker)
if idx == -1:
    print("Marker not found")
    sys.exit(1)
clean = content[:idx].rstrip() + '\n'
open(r'c:\Users\jaque\OneDrive\Escritorio\Antigravity\Documents\UPY\DevSecOps\korebase-django\produccion\forms.py', 'w', encoding='utf-8').write(clean)
print(f'Done — {len(clean.splitlines())} lines')
