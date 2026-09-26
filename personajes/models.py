from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Faccion(models.TextChoices):
    ALIANZA = "alianza", "Alianza"
    HORDA = "horda", "Horda"


class Clase(models.TextChoices):
    GUERRERO = "guerrero", "Guerrero"
    PALADIN = "paladin", "Paladín"
    CAZADOR = "cazador", "Cazador"
    PICARO = "picaro", "Pícaro"
    SACERDOTE = "sacerdote", "Sacerdote"
    CHAMAN = "chaman", "Chamán"
    MAGO = "mago", "Mago"
    BRUJO = "brujo", "Brujo"
    MONJE = "monje", "Monje"
    DRUIDA = "druida", "Druida"
    CABALLERO_MUERTE = "caballero_muerte", "Caballero de la Muerte"
    CAZADOR_DEMONIOS = "cazador_demonios", "Cazador de Demonios"
    EVOCADOR = "evocador", "Evocador"


class Hermandad(models.Model):
    nombre = models.CharField(max_length=100)
    reino = models.CharField(max_length=80)
    faccion = models.CharField(max_length=10, choices=Faccion.choices)
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ["nombre", "reino"]
        constraints = [
            models.UniqueConstraint(fields=["nombre", "reino"], name="hermandad_nombre_reino_unico"),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.reino})"


class Personaje(models.Model):
    nombre = models.CharField(max_length=80)
    reino = models.CharField(max_length=80)
    faccion = models.CharField(max_length=10, choices=Faccion.choices)
    raza = models.CharField(max_length=80)
    clase = models.CharField(max_length=25, choices=Clase.choices)
    especializacion = models.CharField(max_length=80, blank=True)
    nivel = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])
    historia = models.TextField(blank=True)
    hermandad = models.ForeignKey(
        Hermandad,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="personajes",
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-nivel", "nombre"]
        constraints = [
            models.UniqueConstraint(fields=["nombre", "reino"], name="personaje_nombre_reino_unico"),
        ]

    def clean(self):
        if self.hermandad_id and (
            self.hermandad.faccion != self.faccion or self.hermandad.reino.lower() != self.reino.lower()
        ):
            raise ValidationError({"hermandad": "La hermandad debe ser del mismo reino y faccion."})

    def __str__(self):
        return f"{self.nombre} - {self.reino}"


class Aventura(models.Model):
    class Tipo(models.TextChoices):
        MISION = "mision", "Misión"
        MAZMORRA = "mazmorra", "Mazmorra"
        BANDA = "banda", "Banda"
        EXPLORACION = "exploracion", "Exploración"
        PVP = "pvp", "JcJ"

    personaje = models.ForeignKey(Personaje, on_delete=models.CASCADE, related_name="aventuras")
    titulo = models.CharField(max_length=120)
    zona = models.CharField(max_length=100)
    tipo = models.CharField(max_length=12, choices=Tipo.choices)
    fecha = models.DateField()
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ["-fecha", "-id"]

    def __str__(self):
        return f"{self.titulo} - {self.personaje.nombre}"
