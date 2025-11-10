from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Calificacion  # ⬅️ necesario para el serializer de calificaciones

User = get_user_model()


# ----------------- Helpers -----------------

def _primary_role_for(user: User) -> str:
    """
    Rol visible:
    1) primer grupo priorizado por ['Administrador', 'Operador', 'Auditor', 'Usuario']
    2) flags de superuser/staff
    3) 'Usuario'
    """
    groups = list(user.groups.all().values_list("name", flat=True))
    if groups:
        priority = ["Administrador", "Operador", "Auditor", "Usuario"]
        for name in priority:
            if name in groups:
                return name
        return groups[0]
    if user.is_superuser:
        return "Administrador"
    if user.is_staff:
        return "Operador"
    return "Usuario"


def _get_profile(user: User):
    """Devuelve user.profile si existe, sino None (sin romper si no hay OneToOne)."""
    return getattr(user, "profile", None)


def _safe_dt(obj, *names):
    """Devuelve el primer datetime válido encontrado en obj para alguno de los campos dados."""
    for n in names:
        if hasattr(obj, n):
            v = getattr(obj, n)
            if v:
                return v
    return None


def _updated_at_for(user: User):
    """
    Calcula un 'updated_at' razonable.
    """
    prof = _get_profile(user)
    candidates = [
        _safe_dt(user, "updated_at", "modified"),
        _safe_dt(prof, "updated_at", "modified"),
        _safe_dt(user, "last_login"),
        _safe_dt(user, "date_joined"),
        _safe_dt(prof, "created_at", "created"),
    ]
    candidates = [c for c in candidates if c is not None]
    if candidates:
        return max(candidates)
    return timezone.now()


# ----------------- Serializers -----------------

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    phone = serializers.CharField(source="profile.phone", required=False, allow_blank=True, default="")
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_active",
            "role",
            "phone",
            "date_joined",
            "last_login",
            "updated_at",
        ]
        read_only_fields = ["date_joined", "last_login", "role", "updated_at"]

    def get_role(self, obj):
        return _primary_role_for(obj)

    def get_updated_at(self, obj):
        return _updated_at_for(obj)


class UserUpdateSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField(read_only=True)
    phone = serializers.CharField(source="profile.phone", required=False, allow_blank=True)
    updated_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name", "is_active", "phone", "role", "updated_at"]

    def get_role(self, obj):
        return _primary_role_for(obj)

    def get_updated_at(self, obj):
        return _updated_at_for(obj)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})

        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()

        if profile_data:
            prof = _get_profile(instance)
            if prof is not None:
                phone = profile_data.get("phone", None)
                if phone is not None:
                    prof.phone = phone
                    try:
                        prof.save()
                    except Exception:
                        pass

        return instance


class RegisterSerializer(serializers.ModelSerializer):
    """
    Registro abierto (Opción B)
    """
    role = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True, required=False)
    updated_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "password2",
            "is_active",
            "role",
            "phone",
            "updated_at",
        ]

    def get_updated_at(self, obj):
        return _updated_at_for(obj)

    def validate_username(self, v):
        if not v:
            raise serializers.ValidationError("username es obligatorio.")
        if User.objects.filter(username__iexact=v).exists():
            raise serializers.ValidationError("Ese nombre de usuario ya está en uso.")
        return v

    def validate_email(self, v):
        if v and User.objects.filter(email__iexact=v).exists():
            raise serializers.ValidationError("Ese email ya está en uso.")
        return v

    def validate(self, attrs):
        p1 = attrs.get("password") or ""
        p2 = attrs.get("password2") or ""
        if p2 and p1 != p2:
            raise serializers.ValidationError({"password2": "Las contraseñas no coinciden."})
        try:
            validate_password(p1, user=None)
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": " ; ".join(e.messages)})
        return attrs

    def create(self, validated_data):
        role = (validated_data.pop("role", "") or "").strip()
        phone = (validated_data.pop("phone", "") or "").strip()
        validated_data.pop("password2", None)

        password = validated_data.pop("password")
        if "is_active" not in validated_data:
            validated_data["is_active"] = True

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        prof = _get_profile(user)
        if prof and phone:
            prof.phone = phone
            try:
                prof.save()
            except Exception:
                pass

        if not role:
            role = "Usuario"
        grp, _ = Group.objects.get_or_create(name=role)
        user.groups.clear()
        user.groups.add(grp)

        return user


# ---------- Calificaciones ----------

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = [
            "id",
            "rut",
            "razon_social",
            "periodo",
            "tipo_instrumento",
            "folio",
            "monto",
            "moneda",             # ⬅️ NUEVO
            "estado_validacion",
            "observaciones",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
