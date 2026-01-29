from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import JournalEntry, Invoice, ChartOfAccounts


@login_required
def index(request):
    """Financiero dashboard"""
    context = {
        'total_accounts': ChartOfAccounts.objects.filter(active=True).count(),
        'total_journal_entries': JournalEntry.objects.count(),
        'pending_invoices': Invoice.objects.filter(status='issued').count(),
    }
    return render(request, 'financiero/index.html', context)
