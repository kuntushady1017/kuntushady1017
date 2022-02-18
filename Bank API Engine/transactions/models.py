from django.db import models
from django.urls import reverse



class BankTransaction(models.Model):
    transaction_ref = models.CharField(null=False, verbose_name='Transaction Reference', max_length=35, unique=True)
    account = models.CharField(max_length=25, verbose_name='Account Number', null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name='Amount')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = ("b_Transaction")
        verbose_name_plural = ("Bank Transactions")

    def __str__(self):
        return self.transaction_ref

    def get_absolute_url(self):
        return reverse("BankTransaction_detail", kwargs={"pk": self.pk})


class PartnersTransaction(models.Model):
    transaction_ref = models.CharField(max_length=35, null=False, verbose_name='Transaction Reference')
    account = models.CharField(max_length=25, verbose_name='Account Number', null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount', null=False)
    institution = models.CharField(max_length=20, verbose_name='Partner', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = ("partners_transaction")
        verbose_name_plural = ("partners transactions")
    
    def __str__(self) -> str:
        return (self.transaction_ref)
    

class FileUploaded(models.Model):
    name = models.CharField(max_length=20, default='parterns transactions', verbose_name='Partners File')
    file = models.FileField(upload_to='files', null=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = ("Partner File")
        verbose_name_plural = ("Partners Files")
        
    def __str__(self):
        return self.name