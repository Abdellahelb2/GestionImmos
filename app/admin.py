from django.contrib import admin
from .models import CustomUser,BienImmo,client,entrepreneur,Reservation,Message,Favoris

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(BienImmo)
admin.site.register(client)
admin.site.register(entrepreneur)
admin.site.register(Reservation)
admin.site.register(Message)
admin.site.register(Favoris)