from django.db import models

class Role(models.Model):
    # Usa el mismo nombre de campo que ya tenías antes para evitar "alter"
    name = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.name

class UserAccount(models.Model):
    email = models.EmailField(unique=True)
    role  = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="users")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.email

class Calificacion(models.Model):
    rut = models.CharField(max_length=20)
    razon_social = models.CharField(max_length=200)
    periodo = models.CharField(max_length=7)  # 'YYYY-MM'
    tipo_instrumento = models.CharField(max_length=50)
    folio = models.CharField(max_length=30)
    monto = models.IntegerField()
    estado_validacion = models.CharField(max_length=50)
    observaciones = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["rut"]),
            models.Index(fields=["periodo"]),
            models.Index(fields=["tipo_instrumento"]),
            models.Index(fields=["estado_validacion"]),
        ]

    def __str__(self):
        return f"{self.rut} {self.tipo_instrumento} {self.folio}"

class FxRate(models.Model):
    code = models.CharField(max_length=3, unique=True)   # 'CLP','USD','PEN','COP'
    name = models.CharField(max_length=50, default="")
    clp_per_unit = models.DecimalField(max_digits=12, decimal_places=4)
    def __str__(self): return f"{self.code} ({self.clp_per_unit} CLP)"
