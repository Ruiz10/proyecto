from django.db import models

# Create your models here.

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

class Mesa(models.Model):
    numero_mesa = models.IntegerField(unique=True)
    capacidad = models.IntegerField()

    def __str__(self):
        return f"Mesa {self.numero_mesa} - Capacidad {self.capacidad}"

class Reserva(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reserva para {self.cliente} en {self.fecha} a las {self.hora}"
