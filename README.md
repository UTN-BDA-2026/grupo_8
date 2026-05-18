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

Integrantes
* Aguilera Sebastian
* Aguilera Rocío
* Gonzalez Luciana
* Perez Jazmín
* Gualpa Agostina