from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.login,name = 'login'),
    path('validate',views.validate,name = "validate"),
    path('start',views.start,name = 'start'),
    path('stop',views.stop,name = 'stop'),
    path('showdata',views.showdata,name = 'showdata'),
    
]