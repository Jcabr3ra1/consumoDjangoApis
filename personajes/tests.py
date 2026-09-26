from datetime import date

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Aventura, Hermandad, Personaje


class PersonajesApiTests(APITestCase):
    def setUp(self):
        self.hermandad = Hermandad.objects.create(
            nombre="Vigias del Alba", reino="Amanecer", faccion="alianza"
        )
        self.personaje = Personaje.objects.create(
            nombre="Thalren", reino="Amanecer", faccion="alianza",
            raza="humano", clase="mago", nivel=72, hermandad=self.hermandad,
        )
        self.usuario = get_user_model().objects.create_user(username="explorador", password="clave-segura-123")

    def test_lectura_publica_y_escritura_autenticada(self):
        respuesta = self.client.get("/api/personajes/")
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        self.assertEqual(respuesta.data["count"], 1)

        datos = {
            "nombre": "Brumacero", "reino": "Amanecer", "faccion": "alianza",
            "raza": "enano", "clase": "guerrero", "nivel": 35,
        }
        self.assertEqual(self.client.post("/api/personajes/", datos).status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=self.usuario)
        self.assertEqual(self.client.post("/api/personajes/", datos).status_code, status.HTTP_201_CREATED)

    def test_personaje_no_puede_unirse_a_hermandad_de_otra_faccion(self):
        self.client.force_authenticate(user=self.usuario)
        respuesta = self.client.post("/api/personajes/", {
            "nombre": "Sombrario", "reino": "Amanecer", "faccion": "horda",
            "raza": "orco", "clase": "chaman", "nivel": 10,
            "hermandad": self.hermandad.id,
        })
        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("hermandad", respuesta.data)

    def test_filtros_y_resumen(self):
        Personaje.objects.create(
            nombre="Zarok", reino="Fuego", faccion="horda",
            raza="orco", clase="guerrero", nivel=31,
        )
        filtrado = self.client.get("/api/personajes/?faccion=alianza&clase=mago&nivel_min=50")
        self.assertEqual(filtrado.data["count"], 1)
        self.assertEqual(filtrado.data["results"][0]["nombre"], "Thalren")
        self.assertEqual(self.client.get("/api/personajes/?nivel_min=abc").status_code, 400)

        resumen = self.client.get("/api/resumen/")
        self.assertEqual(resumen.data["total_personajes"], 2)
        self.assertEqual(resumen.data["por_faccion"], {"alianza": 1, "horda": 1})

    def test_aventuras_de_un_personaje(self):
        Aventura.objects.create(
            personaje=self.personaje, titulo="Camino entre ruinas", zona="Bosque Viejo",
            tipo="exploracion", fecha=date(2026, 9, 20),
        )
        respuesta = self.client.get(f"/api/personajes/{self.personaje.id}/aventuras/")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.data["count"], 1)
        self.assertEqual(respuesta.data["results"][0]["titulo"], "Camino entre ruinas")

    def test_hermandad_con_miembros_no_cambia_de_faccion(self):
        self.client.force_authenticate(user=self.usuario)
        respuesta = self.client.patch(
            f"/api/hermandades/{self.hermandad.id}/", {"faccion": "horda"}
        )
        self.assertEqual(respuesta.status_code, 400)

    def test_login_entrega_token(self):
        respuesta = self.client.post(
            "/api/auth/token/", {"username": "explorador", "password": "clave-segura-123"}
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("token", respuesta.data)
