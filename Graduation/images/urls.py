from django.urls import path
from . import views



urlpatterns = [
    path('enter/' ,views.enter_image , name='images'),
    path('', views.all, name='all'),
 

]