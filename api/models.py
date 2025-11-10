from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Role(models.Model):
    # Usa el mismo nombre de campo que ya tenías antes para evitar "alter"
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class UserAccount(models.Model):
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="users")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


# === PERFIL ADICIONAL PARA USER (teléfono) ===
class UserProfile(models.Model):
    # Se mantiene referencia directa a User para no romper migraciones existentes
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=32, blank=True, default="")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perfil {self.user.email or self.user.username}"


# === FLAGS por usuario (p.ej. forzar cambio de contraseña) ===
class UserFlag(models.Model):
    # Usamos AUTH_USER_MODEL para ser compatibles si en el futuro personalizas el User
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="flags",
    )
    must_change_password = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Flags({self.user_id}) must_change_password={self.must_change_password}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_user_flags(sender, instance, created, **kwargs):
    """
    Al crear un usuario, garantizamos que exista su registro de flags.
    No altera usuarios existentes; simplemente asegura el 1-1.
    """
    if created:
        UserFlag.objects.get_or_create(user=instance)


class Calificacion(models.Model):
    MONEDAS = (
        ("CLP", "CLP"),
        ("COP", "COP"),
        ("PEN", "PEN"),
        ("USD", "USD"),
    )

    rut = models.CharField(max_length=20)
    razon_social = models.CharField(max_length=200)
    periodo = models.CharField(max_length=7)  # 'YYYY-MM'
    tipo_instrumento = models.CharField(max_length=50)
    folio = models.CharField(max_length=30)
    monto = models.IntegerField()  # almacenado en la unidad propia de 'moneda' o en CLP según tu diseño
    moneda = models.CharField(max_length=3, choices=MONEDAS, default="CLP")  # <-- NUEVO
    estado_validacion = models.CharField(max_length=50)
    observaciones = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["rut"]),
            models.Index(fields=["periodo"]),
            models.Index(fields=["tipo_instrumento"]),
            models.Index(fields=["estado_validacion"]),
            models.Index(fields=["moneda"]),
        ]

    def __str__(self):
        return f"{self.rut} {self.tipo_instrumento} {self.folio} [{self.moneda}] {self.monto}"


class FxRate(models.Model):
    code = models.CharField(max_length=3, unique=True)  # 'CLP','USD','PEN','COP'
    name = models.CharField(max_length=50, default="")
    clp_per_unit = models.DecimalField(max_digits=12, decimal_places=4)

    def __str__(self):
        return f"{self.code} ({self.clp_per_unit} CLP)"
