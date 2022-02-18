from msilib.schema import File
from django.contrib import admin
from transactions.models import BankTransaction, FileUploaded, PartnersTransaction


class BankAdmin(admin.ModelAdmin):
    class Meta:
        model = BankTransaction
        
    list_display = ['transaction_ref', 'account', 'amount']
    ordering = ['id']
    
    
class PartnersAdmin(admin.ModelAdmin):
    class Meta:
        model = PartnersTransaction
        
    list_display = ['transaction_ref', 'account', 'amount', 'institution']
    ordering = ['id']

admin.site.register(BankTransaction, BankAdmin)
admin.site.register(PartnersTransaction, PartnersAdmin)
admin.site.register(FileUploaded)
