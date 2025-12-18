from django.urls import path
from . import views

urlpatterns = [
     path('pay/', views.initiate_payment, name='initiate_payment'),
    path('callback/', views.daraja_callback, name='daraja_callback'),
    path('status/<int:transaction_id>/', views.transaction_status, name='transaction_status')

]