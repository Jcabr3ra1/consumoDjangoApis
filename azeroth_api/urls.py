"""Rutas publicas de la API de personajes."""

from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from personajes.views import AventuraViewSet, HermandadViewSet, PersonajeViewSet, ResumenView

router = DefaultRouter()
router.register("personajes", PersonajeViewSet, basename="personaje")
router.register("hermandades", HermandadViewSet, basename="hermandad")
router.register("aventuras", AventuraViewSet, basename="aventura")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/token/", obtain_auth_token, name="obtener-token"),
    path("api/resumen/", ResumenView.as_view(), name="resumen"),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]
