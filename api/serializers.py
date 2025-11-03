from rest_framework import serializers
from .models import Role, UserAccount, Calificacion

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name"]

class UserAccountSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source="role.name", read_only=True)
    class Meta:
        model = UserAccount
        fields = ["id", "email", "role", "role_name", "created_at", "updated_at"]

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = [
            "id","rut","razon_social","periodo","tipo_instrumento",
            "folio","monto","estado_validacion","observaciones",
            "created_at","updated_at"
        ]
