# Crónicas de Azeroth

API REST educativa para crear personajes inspirados en **World of Warcraft**, agruparlos en hermandades y registrar sus aventuras. Los personajes y las historias del ejemplo son originales. Este proyecto no es oficial ni usa datos de cuentas de Blizzard.

## Qué incluye

- CRUD de personajes con facción, raza, clase, especialización, nivel, reino e historia.
- Hermandades con validación de facción y reino de sus miembros.
- Aventuras asociadas a cada personaje.
- Búsqueda por nombre y filtros por facción, clase, reino y nivel mínimo.
- Resumen con totales, distribuciones y personajes destacados.
- Lectura pública; para crear, modificar o borrar se requiere un usuario autenticado.

## Preparación

Requiere Python 3.14. Desde la carpeta del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata demo
python manage.py createsuperuser
python manage.py runserver
```

La API navegable queda en `http://127.0.0.1:8000/api/` y el panel administrativo en `http://127.0.0.1:8000/admin/`. `loaddata demo` agrega tres personajes inventados; es opcional.

## Rutas

| Método | Ruta | Uso |
| --- | --- | --- |
| GET, POST | `/api/personajes/` | Listar o crear personajes |
| GET, PUT, PATCH, DELETE | `/api/personajes/{id}/` | Consultar, editar o borrar un personaje |
| GET | `/api/personajes/{id}/aventuras/` | Aventuras de un personaje |
| GET, POST | `/api/hermandades/` | Listar o crear hermandades |
| GET, PUT, PATCH, DELETE | `/api/hermandades/{id}/` | Consultar, editar o borrar una hermandad |
| GET, POST | `/api/aventuras/` | Listar o crear aventuras |
| GET, PUT, PATCH, DELETE | `/api/aventuras/{id}/` | Consultar, editar o borrar una aventura |
| GET | `/api/resumen/` | Estadísticas del catálogo |
| POST | `/api/auth/token/` | Obtener token con `username` y `password` |

La lista de personajes acepta `faccion`, `clase`, `reino`, `nombre` y `nivel_min`; la de hermandades acepta `faccion` y `reino`; la de aventuras acepta `personaje` y `tipo`. Las listas están paginadas de 10 en 10.

Ejemplo de consulta: `GET /api/personajes/?faccion=alianza&clase=mago&nivel_min=50`.

Ejemplo de personaje nuevo:

```json
{
  "nombre": "Lunargenta",
  "reino": "Amanecer",
  "faccion": "alianza",
  "raza": "elfa de la noche",
  "clase": "druida",
  "especializacion": "restauracion",
  "nivel": 30,
  "historia": "Recorre bosques y protege a sus aliados.",
  "hermandad": 1
}
```

Para escribir desde Postman, primero envía `username` y `password` a `/api/auth/token/`; después usa la cabecera `Authorization: Token TU_TOKEN`. También puedes iniciar sesión en la API navegable mediante `/api-auth/login/`.

## Pruebas

```powershell
python manage.py test
```

Antes de publicar fuera de un entorno local, configura `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0` y `DJANGO_ALLOWED_HOSTS`. La base de datos local y el entorno virtual están excluidos de Git.

Referencia de terminología del juego: [razas jugables de World of Warcraft](https://worldofwarcraft.blizzard.com/en-gb/game/races).
