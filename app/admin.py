from django.contrib import admin
from .models import CustomUser,BienImmo,client,entrepreneur

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(BienImmo)
admin.site.register(client)
admin.site.register(entrepreneur)