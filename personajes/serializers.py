from rest_framework import serializers

from .models import Aventura, Hermandad, Personaje


class HermandadSerializer(serializers.ModelSerializer):
    miembros = serializers.SerializerMethodField()

    class Meta:
        model = Hermandad
        fields = ["id", "nombre", "reino", "faccion", "descripcion", "miembros"]

    def get_miembros(self, obj):
        return obj.personajes.count()

    def validate(self, attrs):
        if self.instance and self.instance.personajes.exists():
            faccion = attrs.get("faccion", self.instance.faccion)
            reino = attrs.get("reino", self.instance.reino)
            if faccion != self.instance.faccion or reino.lower() != self.instance.reino.lower():
                raise serializers.ValidationError(
                    "No se puede cambiar el reino o la faccion de una hermandad con personajes."
                )
        return attrs


class PersonajeSerializer(serializers.ModelSerializer):
    hermandad_nombre = serializers.CharField(source="hermandad.nombre", read_only=True)

    class Meta:
        model = Personaje
        fields = [
            "id", "nombre", "reino", "faccion", "raza", "clase", "especializacion",
            "nivel", "historia", "hermandad", "hermandad_nombre", "creado_en",
        ]
        read_only_fields = ["id", "creado_en"]

    def validate(self, attrs):
        hermandad = attrs.get("hermandad", self.instance.hermandad if self.instance else None)
        faccion = attrs.get("faccion", self.instance.faccion if self.instance else None)
        reino = attrs.get("reino", self.instance.reino if self.instance else None)
        if hermandad and (hermandad.faccion != faccion or hermandad.reino.lower() != reino.lower()):
            raise serializers.ValidationError(
                {"hermandad": "La hermandad debe ser del mismo reino y faccion que el personaje."}
            )
        return attrs


class AventuraSerializer(serializers.ModelSerializer):
    personaje_nombre = serializers.CharField(source="personaje.nombre", read_only=True)

    class Meta:
        model = Aventura
        fields = ["id", "personaje", "personaje_nombre", "titulo", "zona", "tipo", "fecha", "descripcion"]
        read_only_fields = ["id"]
