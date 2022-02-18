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

name = ('X', 'Y', 'x', 'y')
header = 'Institution-Name'

@api_view(['POST'])
@parser_classes([FormParser, MultiPartParser, FileUploadParser])
@permission_classes([IsAuthenticated])
def transaction_post(request):
    if request.method == 'POST':
        print(request.data, request.headers)
        myheader = request.headers['Institution-Name']
        if header not in request.headers:
            msg = str("Please in your header add a variable named institution-name with your company letter")
            return Response({'Failure': msg, 'status_ code': status.HTTP_428_PRECONDITION_REQUIRED}, status.HTTP_428_PRECONDITION_REQUIRED) 
        elif myheader not in name:
            msg = str("Please in your header write the company letter given X or Y or x or y")
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
                msg = str("Uploaded successful")
        return Response({"data": file_serializer.data, "message":msg}, status.HTTP_200_OK)    

def index(request):
    queryset = BankTransaction.objects.distinct()
    print(queryset)
    return HttpResponse(request, STATUS)