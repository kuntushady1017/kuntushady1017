from django.urls import path
from transactions import views

urlpatterns = [
    path('', views.index, name='home'),
    path('bank-b-engine/api/V1/transactions', views.transaction_post, name='transactions')
]
