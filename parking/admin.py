from django.contrib import admin
from .models import *

admin.site.register(Building)
admin.site.register(Tenant)
admin.site.register(Staff)
admin.site.register(Pass)