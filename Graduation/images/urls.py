from django.urls import path
from . import views



urlpatterns = [
    path('' ,views.enter_image , name='images'),
    path('photos/', views.all, name='all'),
 

]