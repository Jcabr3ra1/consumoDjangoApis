from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Aventura, Hermandad, Personaje
from .serializers import AventuraSerializer, HermandadSerializer, PersonajeSerializer


class HermandadViewSet(viewsets.ModelViewSet):
    serializer_class = HermandadSerializer
    queryset = Hermandad.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if faccion := self.request.query_params.get("faccion"):
            queryset = queryset.filter(faccion=faccion)
        if reino := self.request.query_params.get("reino"):
            queryset = queryset.filter(reino__iexact=reino)
        return queryset


class PersonajeViewSet(viewsets.ModelViewSet):
    serializer_class = PersonajeSerializer
    queryset = Personaje.objects.select_related("hermandad")

    def get_queryset(self):
        queryset = super().get_queryset()
        filtros = self.request.query_params
        if faccion := filtros.get("faccion"):
            queryset = queryset.filter(faccion=faccion)
        if clase := filtros.get("clase"):
            queryset = queryset.filter(clase=clase)
        if reino := filtros.get("reino"):
            queryset = queryset.filter(reino__iexact=reino)
        if nombre := filtros.get("nombre"):
            queryset = queryset.filter(nombre__icontains=nombre)
        if nivel_min := filtros.get("nivel_min"):
            try:
                nivel = int(nivel_min)
            except ValueError as exc:
                raise ValidationError({"nivel_min": "Debe ser un numero entero."}) from exc
            if nivel < 1:
                raise ValidationError({"nivel_min": "Debe ser mayor que cero."})
            queryset = queryset.filter(nivel__gte=nivel)
        return queryset

    @action(detail=True, methods=["get"])
    def aventuras(self, request, pk=None):
        personaje = self.get_object()
        queryset = personaje.aventuras.all()
        pagina = self.paginate_queryset(queryset)
        if pagina is not None:
            return self.get_paginated_response(AventuraSerializer(pagina, many=True).data)
        return Response(AventuraSerializer(queryset, many=True).data)


class AventuraViewSet(viewsets.ModelViewSet):
    serializer_class = AventuraSerializer
    queryset = Aventura.objects.select_related("personaje")

    def get_queryset(self):
        queryset = super().get_queryset()
        if tipo := self.request.query_params.get("tipo"):
            queryset = queryset.filter(tipo=tipo)
        if personaje := self.request.query_params.get("personaje"):
            try:
                personaje_id = int(personaje)
            except ValueError as exc:
                raise ValidationError({"personaje": "Debe ser un ID entero."}) from exc
            queryset = queryset.filter(personaje_id=personaje_id)
        return queryset


class ResumenView(APIView):
    def get(self, request):
        por_faccion = Personaje.objects.values("faccion").annotate(total=Count("id"))
        por_clase = Personaje.objects.values("clase").annotate(total=Count("id"))
        destacados = Personaje.objects.order_by("-nivel", "nombre").values(
            "id", "nombre", "reino", "clase", "nivel"
        )[:5]
        return Response({
            "total_personajes": Personaje.objects.count(),
            "total_hermandades": Hermandad.objects.count(),
            "total_aventuras": Aventura.objects.count(),
            "por_faccion": {item["faccion"]: item["total"] for item in por_faccion},
            "por_clase": {item["clase"]: item["total"] for item in por_clase},
            "destacados": list(destacados),
        })
