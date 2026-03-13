"""
Financiero Views - Accounting & Finance CRUD
KoreBase ERP System
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum, Q, DecimalField, Value
from django.db.models.functions import Coalesce
from decimal import Decimal

from .models import ChartOfAccounts, JournalEntry, JournalEntryLine, Invoice
from .forms import (
    ChartOfAccountsForm, JournalEntryForm, JournalEntryLineFormSet, InvoiceForm
)


# ==================== DASHBOARD ====================

@login_required
def index(request):
    """Financiero dashboard with real KPIs"""
    total_accounts = ChartOfAccounts.objects.filter(active=True).count()
    total_journal_entries = JournalEntry.objects.count()
    pending_invoices = Invoice.objects.filter(status='issued').count()
    total_invoices = Invoice.objects.count()

    # Calculate totals from invoices
    income_total = Invoice.objects.filter(
        invoice_type='customer', status__in=['issued', 'paid']
    ).aggregate(total=Coalesce(Sum('total'), Value(Decimal('0.00')), output_field=DecimalField()))['total']

    expense_total = Invoice.objects.filter(
        invoice_type='supplier', status__in=['issued', 'paid']
    ).aggregate(total=Coalesce(Sum('total'), Value(Decimal('0.00')), output_field=DecimalField()))['total']

    context = {
        'total_accounts': total_accounts,
        'total_journal_entries': total_journal_entries,
        'pending_invoices': pending_invoices,
        'total_invoices': total_invoices,
        'income_total': income_total,
        'expense_total': expense_total,
        'net_margin': income_total - expense_total,
        'recent_entries': JournalEntry.objects.select_related('created_by').order_by('-created_at')[:5],
        'recent_invoices': Invoice.objects.order_by('-created_at')[:5],
    }
    return render(request, 'financiero/index.html', context)


# ==================== CHART OF ACCOUNTS ====================

@login_required
def accounts_list(request):
    """List all accounts in the chart of accounts"""
    accounts = ChartOfAccounts.objects.filter(active=True).order_by('account_code')

    account_type = request.GET.get('type')
    if account_type:
        accounts = accounts.filter(account_type=account_type)

    query = request.GET.get('q')
    if query:
        accounts = accounts.filter(
            Q(account_code__icontains=query) |
            Q(account_name__icontains=query)
        )

    context = {
        'accounts': accounts,
        'account_types': ChartOfAccounts.ACCOUNT_TYPES,
        'current_type': account_type or '',
        'search_query': query or '',
    }
    return render(request, 'financiero/accounts_list.html', context)


@login_required
def account_create(request):
    """Create a new account"""
    if request.method == 'POST':
        form = ChartOfAccountsForm(request.POST)
        if form.is_valid():
            account = form.save()
            messages.success(request, f'Cuenta "{account.account_name}" creada exitosamente.')
            return redirect('financiero:accounts_list')
    else:
        form = ChartOfAccountsForm()

    return render(request, 'financiero/account_form.html', {'form': form, 'title': 'Nueva Cuenta'})


@login_required
def account_edit(request, pk):
    """Edit an existing account"""
    account = get_object_or_404(ChartOfAccounts, pk=pk)

    if request.method == 'POST':
        form = ChartOfAccountsForm(request.POST, instance=account)
        if form.is_valid():
            account = form.save()
            messages.success(request, f'Cuenta "{account.account_name}" actualizada.')
            return redirect('financiero:accounts_list')
    else:
        form = ChartOfAccountsForm(instance=account)

    return render(request, 'financiero/account_form.html', {
        'form': form, 'title': 'Editar Cuenta', 'account': account
    })


# ==================== JOURNAL ENTRIES ====================

@login_required
def journal_list(request):
    """List all journal entries"""
    entries = JournalEntry.objects.select_related('created_by').order_by('-entry_date', '-created_at')

    query = request.GET.get('q')
    if query:
        entries = entries.filter(
            Q(entry_number__icontains=query) |
            Q(description__icontains=query)
        )

    show_reversed = request.GET.get('reversed')
    if show_reversed == '1':
        entries = entries.filter(reversed=True)
    elif show_reversed == '0':
        entries = entries.filter(reversed=False)

    context = {
        'entries': entries,
        'search_query': query or '',
        'show_reversed': show_reversed or '',
    }
    return render(request, 'financiero/journal_list.html', context)


@login_required
@transaction.atomic
def journal_create(request):
    """Create a new journal entry with lines. Validates debits == credits."""
    if request.method == 'POST':
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.created_by = request.user
            # Temporarily save to get PK for formset
            entry.save()

            formset = JournalEntryLineFormSet(request.POST, instance=entry)
            if formset.is_valid():
                lines = formset.save(commit=False)

                # Validate debits == credits
                total_debit = sum(line.debit for line in lines)
                total_credit = sum(line.credit for line in lines)

                if total_debit != total_credit:
                    # Rollback: delete the entry (transaction.atomic handles this)
                    entry.delete()
                    messages.error(
                        request,
                        f'El total de débitos (${total_debit}) debe ser igual al total de créditos (${total_credit}).'
                    )
                    # Re-render with formset
                    form = JournalEntryForm(request.POST)
                    formset = JournalEntryLineFormSet(request.POST)
                    return render(request, 'financiero/journal_create.html', {
                        'form': form, 'formset': formset
                    })

                for line in lines:
                    line.save()

                messages.success(request, f'Asiento "{entry.entry_number}" creado exitosamente.')
                notify(request.user, f'Nuevo Asiento Contable: {entry.entry_number}', 'info', f'/financiero/journal/{entry.pk}/')
                return redirect('financiero:journal_detail', pk=entry.pk)
            else:
                # Formset invalid — rollback
                entry.delete()
                messages.error(request, 'Corrige los errores en las líneas del asiento.')
        else:
            formset = JournalEntryLineFormSet(request.POST)
    else:
        form = JournalEntryForm()
        formset = JournalEntryLineFormSet()

    return render(request, 'financiero/journal_create.html', {
        'form': form, 'formset': formset
    })


@login_required
def journal_detail(request, pk):
    """View a journal entry with all its lines"""
    entry = get_object_or_404(JournalEntry, pk=pk)
    lines = entry.lines.select_related('account').all()

    total_debit = lines.aggregate(
        total=Coalesce(Sum('debit'), Value(Decimal('0.00')), output_field=DecimalField())
    )['total']
    total_credit = lines.aggregate(
        total=Coalesce(Sum('credit'), Value(Decimal('0.00')), output_field=DecimalField())
    )['total']

    context = {
        'entry': entry,
        'lines': lines,
        'total_debit': total_debit,
        'total_credit': total_credit,
    }
    return render(request, 'financiero/journal_detail.html', context)


@login_required
@transaction.atomic
def journal_reverse(request, pk):
    """Create a reversal entry for a journal entry"""
    entry = get_object_or_404(JournalEntry, pk=pk)

    if request.method == 'POST':
        try:
            reversal = entry.create_reversal(
                user=request.user,
                description=request.POST.get('description', 'Reverso')
            )
            messages.success(
                request,
                f'Asiento "{entry.entry_number}" revertido. Nuevo asiento: "{reversal.entry_number}".'
            )
            return redirect('financiero:journal_detail', pk=reversal.pk)
        except ValueError as e:
            messages.error(request, str(e))

    return redirect('financiero:journal_detail', pk=pk)


# ==================== INVOICES ====================

@login_required
def invoice_list(request):
    """List all invoices"""
    invoices = Invoice.objects.select_related('created_by').order_by('-invoice_date')

    query = request.GET.get('q')
    if query:
        invoices = invoices.filter(
            Q(invoice_number__icontains=query) |
            Q(customer_supplier__icontains=query)
        )

    status_filter = request.GET.get('status')
    if status_filter:
        invoices = invoices.filter(status=status_filter)

    type_filter = request.GET.get('type')
    if type_filter:
        invoices = invoices.filter(invoice_type=type_filter)

    context = {
        'invoices': invoices,
        'status_choices': Invoice.STATUS_CHOICES,
        'type_choices': Invoice.TYPE_CHOICES,
        'current_status': status_filter or '',
        'current_type': type_filter or '',
        'search_query': query or '',
    }
    return render(request, 'financiero/invoice_list.html', context)


@login_required
def invoice_create(request):
    """Create a new invoice"""
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.created_by = request.user
            invoice.save()
            messages.success(request, f'Factura "{invoice.invoice_number}" creada exitosamente.')
            notify(request.user, f'Nueva Factura: {invoice.invoice_number}', 'info', f'/financiero/invoice/{invoice.pk}/')
            return redirect('financiero:invoice_list')
    else:
        form = InvoiceForm()

    return render(request, 'financiero/invoice_form.html', {'form': form, 'title': 'Nueva Factura'})


@login_required
def invoice_edit(request, pk):
    """Edit an existing invoice (only if draft)"""
    invoice = get_object_or_404(Invoice, pk=pk)

    if invoice.status != 'draft':
        messages.error(request, 'Solo se pueden editar facturas en estado Borrador.')
        return redirect('financiero:invoice_list')

    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            invoice = form.save()
            messages.success(request, f'Factura "{invoice.invoice_number}" actualizada.')
            return redirect('financiero:invoice_list')
    else:
        form = InvoiceForm(instance=invoice)

    return render(request, 'financiero/invoice_form.html', {
        'form': form, 'title': 'Editar Factura', 'invoice': invoice
    })


@login_required
def invoice_status(request, pk):
    """Change invoice status with valid transitions"""
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')

        # Valid state transitions
        valid_transitions = {
            'draft': ['issued', 'cancelled'],
            'issued': ['paid', 'cancelled'],
            'paid': [],
            'cancelled': [],
        }

        allowed = valid_transitions.get(invoice.status, [])
        if new_status not in allowed:
            messages.error(
                request,
                f'No se puede cambiar de "{invoice.get_status_display()}" a "{new_status}".'
            )
            return redirect('financiero:invoice_list')

        invoice.status = new_status
        invoice.save()

        status_labels = dict(Invoice.STATUS_CHOICES)
        messages.success(
            request,
            f'Factura "{invoice.invoice_number}" ahora está: {status_labels.get(new_status, new_status)}.'
        )

    return redirect('financiero:invoice_list')
