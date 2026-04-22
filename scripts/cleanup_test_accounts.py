from core.models import CustomUser, Company, CompanyMembership, CompanyInvitation

emails_to_delete = ['ricardohawbra@gmail.com', 'nestorucuc@gmail.com']

for email in emails_to_delete:
    user = CustomUser.objects.filter(email__iexact=email).first()
    if not user:
        print(f'  [=] No encontrado: {email}')
        continue

    company = user.company
    company_name = company.name if company else 'Sin empresa'
    print(f'  [~] Procesando: {user.username} ({email}) @ {company_name}')

    # Borrar invitaciones relacionadas a la empresa del usuario
    if company:
        inv_del = CompanyInvitation.objects.filter(company=company).delete()
        print(f'      - Invitaciones eliminadas: {inv_del}')
        mem_del = CompanyMembership.objects.filter(company=company).delete()
        print(f'      - Membresías eliminadas: {mem_del}')

    # Borrar el usuario (CASCADE elimina OTPs, notificaciones, etc.)
    user.delete()
    print(f'      - Usuario eliminado: {email}')

    # Borrar la empresa si quedó vacía
    if company:
        remaining = CustomUser.objects.filter(company=company).count()
        if remaining == 0:
            company.delete()
            print(f'      - Empresa eliminada: {company_name}')
        else:
            print(f'      - Empresa conservada ({remaining} usuario(s)): {company_name}')

# Limpiar invitaciones pendientes residuales para esos correos en cualquier empresa
leftover = CompanyInvitation.objects.filter(email__in=emails_to_delete)
lcount = leftover.count()
if lcount > 0:
    leftover.delete()
    print(f'  [~] Invitaciones pendientes residuales eliminadas: {lcount}')

print()
print('--- Estado final ---')
for email in emails_to_delete:
    exists = CustomUser.objects.filter(email__iexact=email).exists()
    result = 'AUN EXISTE (!)' if exists else 'Eliminado correctamente'
    print(f'  {email}: {result}')
