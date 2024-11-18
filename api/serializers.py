from rest_framework import serializers
from .models import Cliente, Mesa, Reserva

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'email', 'telefono']

class MesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesa
        fields = ['id', 'numero_mesa', 'capacidad']

class ReservaSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer()
    mesa = MesaSerializer()

    class Meta:
        model = Reserva
        fields = ['id', 'fecha', 'hora', 'cliente', 'mesa']
