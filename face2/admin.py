from multiprocessing import Manager
from django.contrib import admin

# Register your models here.
from .models import Register,Manager

admin.site.register(Register)
admin.site.register(Manager)
