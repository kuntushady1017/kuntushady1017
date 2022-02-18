from dataclasses import fields
from rest_framework import serializers
from .models import FileUploaded, BankTransaction, PartnersTransaction


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUploaded
        fields = '__all__'
        
        