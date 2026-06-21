# grupo_8

## Buscador de productos con FastAPI y PostgreSQL

Este proyecto implementa una aplicación de búsqueda sobre datasets masivos (millones de productos), diseñada para ser escalable y eficiente.

🔹 Arquitectura de datos

La base de datos se organiza en 6 tablas principales:

# productos → núcleo con campos esenciales (asin, title, brand, price, description, date, main_cat).

# categorias → jerarquía completa de categorías por producto.

# imagenes → URLs de imágenes en distintos formatos.

# relaciones → vínculos also_buy y also_view entre productos.

# ranking → posiciones de popularidad en Amazon por categoría.

# caracteristicas → lista de features adicionales.

🔹 Backend
FastAPI expone endpoints REST para búsquedas y filtrados.

Integración con PostgreSQL usando índices avanzados (BTREE, GIN) y Full‑Text Search (tsvector, tsquery).

Redis para caching de resultados frecuentes.

Materialized Views para precalcular catálogos (ej. top productos por categoría).

Particiones en tablas grandes para mejorar rendimiento.

🔹 Objetivo
Construir un buscador tipo “Google interno” que permita:

Consultas rápidas por título, marca o categoría.

Ordenar resultados por precio, relevancia o ranking.

Escalar a millones de registros sin comprometer rendimiento.

### Levantar la aplicación con Docker Compose

1. Requisitos previos

-Tener instalados Docker

-Contar con una base de datos PostgreSQL creada previamente.

-Configurar un archivo .env en la raíz del proyecto con las credenciales de conexión a la base de datos.

2. Migraciones con Alembic

Antes de usar la API, es necesario aplicar las migraciones para que la base de datos tenga las tablas e índices correctos.

# Crear una nueva migración (si cambiaste modelos)

alembic revision --autogenerate -m "mensaje de la migración"

# Aplicar todas las migraciones pendientes

alembic upgrade head

3. Ejecutar en la carpeta docker del proyecto:

docker compose up --build

Esto construye la imagen y levanta el servicio backend.

La API quedará disponible en: http://localhost:8000

4. Verificación

Podés comprobar que la API está corriendo y conectada a la base accediendo a la documentación interactiva:http://localhost:8000/docs

📌 Notas importantes
El docker-compose.yml está pensado para levantar la API. La base de datos debe estar corriendo aparte (local, contenedor independiente o nube).

Las migraciones con Alembic no se aplican automáticamente: cada vez que cambies los modelos, generá una nueva migración y aplicala.

Integrantes

- Aguilera Sebastian
- Aguilera Rocío
- Gonzalez Luciana
- Perez Jazmín
- Gualpa Agostina
