from django.contrib import admin
from .models import Cliente, Mesa, Reserva
# Register your models here.
admin.site.register(Cliente)
admin.site.register(Mesa)
admin.site.register(Reserva)
