from django.contrib import admin
from .models import ChartOfAccounts, JournalEntry, JournalEntryLine, Invoice


class JournalEntryLineInline(admin.TabularInline):
    model = JournalEntryLine
    extra = 2
    fields = ['account', 'debit', 'credit', 'description']


@admin.register(ChartOfAccounts)
class ChartOfAccountsAdmin(admin.ModelAdmin):
    list_display = ['account_code', 'account_name', 'account_type', 'balance', 'active']
    list_filter = ['account_type', 'active']
    search_fields = ['account_code', 'account_name']
    ordering = ['account_code']


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['entry_number', 'entry_date', 'description', 'created_by', 'reversed']
    list_filter = ['reversed', 'entry_date']
    search_fields = ['entry_number', 'description']
    readonly_fields = ['created_at', 'created_by', 'reversed', 'reversal_of']
    inlines = [JournalEntryLineInline]
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def has_change_permission(self, request, obj=None):
        # Journal entries are immutable
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Cannot delete journal entries
        return False


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'invoice_type', 'customer_supplier', 'invoice_date', 'total', 'status']
    list_filter = ['invoice_type', 'status', 'invoice_date']
    search_fields = ['invoice_number', 'customer_supplier']
    readonly_fields = ['created_at', 'created_by']
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
