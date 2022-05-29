from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.index,name = 'index'),
    path('start',views.start,name = 'start'),
    path('stop',views.stop,name = 'stop'),
    path('showdata',views.showdata,name = 'showdata'),
    
]