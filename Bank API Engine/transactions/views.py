import io
import pandas as pd
from telnetlib import STATUS
from django.http import HttpResponse
from django.shortcuts import render
from .models import BankTransaction, FileUploaded, PartnersTransaction
from .serializers import FileSerializer
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Count, Sum

name = ('X', 'Y', 'x', 'y')
header = 'HTTP_INSTITUTION_NAME'

@api_view(['POST'])
@parser_classes([FormParser, MultiPartParser, FileUploadParser])
@permission_classes([IsAuthenticated])
def transaction_post(request):
    if request.method == 'POST':
        print(request.headers, request.META)
        if request.META.get(header) == None:
            msg = str("Please in your header add a variable named institution-name with your company letter")
            return Response({'Failure': msg, 'status_ code': status.HTTP_428_PRECONDITION_REQUIRED}, status.HTTP_428_PRECONDITION_REQUIRED) 
        elif request.headers['Institution-Name'] not in name:
            msg = str("Please in your header parameters institution-name write the letter given X or Y or x or y of the company")
            return Response({'Failure': msg, 'status_ code': status.HTTP_428_PRECONDITION_REQUIRED}, status.HTTP_428_PRECONDITION_REQUIRED)
        else:
            file_serializer = FileSerializer(data=request.data)
            if file_serializer.is_valid():
                file_obj = request.FILES['file']
                data_file = request.data.get('file')
                print(file_obj)
                if file_obj.content_type == 'text/csv':
                    data_set = data_file.read().decode('UTF-8')
                    io_string = io.StringIO(data_set)
                    csv_file = pd.read_csv(io_string, low_memory=False)
                    columns = list(csv_file.columns.values)
                    transaction_ref,account,amount = columns[0], columns[1], columns[2]
                    print('csv file', data_set)
                    paterner = request.headers['Institution-Name']
                    instance = [
                        PartnersTransaction(
                            transaction_ref=row[transaction_ref],
                            account=row[account],
                            amount=row[amount],
                            institution=paterner
                        )
                        for index, row in csv_file.iterrows()
                        ]
                    
                    PartnersTransaction.objects.bulk_create(instance)
                    
                    
                    
                elif file_obj.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                    excel_file = pd.read_excel(data_file)
                    columns = list(excel_file.columns.values)
                    transaction_ref,account,amount = columns[0], columns[1], columns[2]
                    paterner = request.headers['Institution-Name']
                    instance = [
                        PartnersTransaction(
                            transaction_ref=row[transaction_ref],
                            account=row[account],
                            amount=row[amount],
                            institution=paterner
                        )
                        for index, row in excel_file.iterrows()
                        ]
                    
                    PartnersTransaction.objects.bulk_create(instance)
                    print('excel file')
                else:
                    msg = str("The file sent has no extesion of .csv or .xlsx")
                    return Response({"Failure":msg, "status code": status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}, status.HTTP_400_BAD_REQUEST)
                file_serializer.save()
                msg = str("Uploaded successful")
        return Response({"data": file_serializer.data, "message":msg}, status.HTTP_200_OK)
    msg2 = str("Uploaded failed")
    return Response({"data": file_serializer.errors, "message": msg2}, status.HTTP_400_BAD_REQUEST)    


def index(request):
    queryset = BankTransaction.objects.all()
    partners_x = PartnersTransaction.objects.all().filter(institution__icontains='x').filter(institution__contains='X')
    
    
     
    return HttpResponse(request, STATUS)