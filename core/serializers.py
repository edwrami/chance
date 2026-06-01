from rest_framework import serializers
from .models import *

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Usuario
        fields = '__all__'
        read_only_fields = ['activo', 'rol', 'empresario']
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = Usuario.objects.create(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

class LoteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loteria
        fields = '__all__'
        read_only_fields = ['empresario']

class PlanPremioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanPremio
        fields = '__all__'
        read_only_fields = ['empresario']

class TopeNumeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopeNumero
        fields = '__all__'
        read_only_fields = ['empresario', 'acumulado_actual']

class ApuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apuesta
        fields = '__all__'
        read_only_fields = ['empresario', 'fecha_hora', 'premio_potencial']

class ComisionVendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComisionVendedor
        fields = '__all__'
        read_only_fields = ['empresario']
