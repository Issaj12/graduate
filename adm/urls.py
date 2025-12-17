from django.urls import path
from . import views
urlpatterns = [


    path('dashboard/', views.dashboard, name='dashboard'),

    # users operation
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.user_create, name='user_create'),
    path('users/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:user_id>/delete/', views.user_delete, name='user_delete'),

    # message operations
  
    path('messages/', views.message_list, name='adm_message_list'),
    path('messages/create/', views.message_create, name='adm_message_create'),
    path('messages/<int:pk>/edit/', views.message_update, name='adm_message_update'),
    path('messages/<int:pk>/delete/', views.message_delete, name='adm_message_delete'),

# contact operations

    path('contacts/', views.contact_list, name='adm_contact_list'),
    path('contacts/create/', views.contact_create, name='adm_contact_create'),
    path('contacts/<int:pk>/edit/', views.contact_update, name='adm_contact_update'),
    path('contacts/<int:pk>/delete/', views.contact_delete, name='adm_contact_delete'),


# images operations

    path('images/', views.image_list, name='adm_image_list'),
    path('images/create/', views.image_create, name='adm_image_create'),
    path('images/<int:pk>/edit/', views.image_update, name='adm_image_update'),
    path('images/<int:pk>/delete/', views.image_delete, name='adm_image_delete'),


# payments operation

    path('payments/', views.payment_list, name='adm_payment_list'),
    path('payments/create/', views.payment_create, name='adm_payment_create'),
    path('payments/<int:pk>/edit/', views.payment_update, name='adm_payment_update'),
    path('payments/<int:pk>/delete/', views.payment_delete, name='adm_payment_delete'),
    path('payments/download/', views.payment_download_csv, name='adm_payment_download'),
]



