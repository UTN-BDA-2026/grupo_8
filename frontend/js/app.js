const API_BASE_URL = "http://localhost:8000";

// --- NUEVA FUNCIÓN: Filtrar por Categoría ---
async function filtrarPorCategoria(boton) {
  const idCategoria = boton.getAttribute("data-id");
  const contenedor = document.getElementById("resultados");

  // Efecto visual: Desmarcar botones anteriores y marcar el actual como activo
  document
    .querySelectorAll(".category-btn")
    .forEach((btn) => btn.classList.remove("active"));
  boton.classList.add("active");

  // Limpiar el buscador de texto para no confundir al usuario
  document.getElementById("inputBusqueda").value = "";

  contenedor.innerHTML =
    "<div class='status-msg'>Cargando los productos con mejor ranking...</div>";

  try {
    // Apuntamos a tu nuevo endpoint pasándole los parámetros requeridos
    const response = await fetch(
      `${API_BASE_URL}/categorias/buscar-por-categoria?categoria=${idCategoria}&page=1&size=20`,
    );

    if (!response.ok) {
      if (response.status === 404) {
        contenedor.innerHTML =
          "<div class='status-msg'>No se encontraron productos rankeados en esta categoría.</div>";
      } else {
        throw new Error("Error en el servidor");
      }
      return;
    }

    const productos = await response.json();
    renderizarProductos(productos);
  } catch (error) {
    contenedor.innerHTML =
      "<div class='status-msg' style='color:red;'>⚠️ Error al conectar con el endpoint de categorías.</div>";
    console.error(error);
  }
}

// --- Modificada: Ejecutar búsqueda por Texto ---
async function ejecutarBusqueda() {
  const query = document.getElementById("inputBusqueda").value.trim();
  const contenedor = document.getElementById("resultados");

  if (!query) {
    alert("Por favor, escribe algo para buscar.");
    return;
  }

  // Si busca por texto, quitamos la selección visual de las categorías
  document
    .querySelectorAll(".category-btn")
    .forEach((btn) => btn.classList.remove("active"));

  contenedor.innerHTML =
    "<div class='status-msg'>Buscando productos de forma ultra rápida...</div>";

  try {
    const response = await fetch(
      `${API_BASE_URL}/productos/buscar?titulo=${query}&limit=20`,
    );
    const productos = await response.json();
    renderizarProductos(productos);
  } catch (error) {
    contenedor.innerHTML =
      "<div class='status-msg' style='color:red;'>⚠️ Error al conectar con la API de FastAPI.</div>";
    console.error(error);
  }
}

// --- FUNCIÓN COMPARTIDA: Renderizar tarjetas en pantalla ---
function renderizarProductos(productos) {
  const contenedor = document.getElementById("resultados");
  contenedor.innerHTML = ""; // Limpiar pantalla

  if (productos.length === 0) {
    contenedor.innerHTML =
      "<div class='status-msg'>No se encontraron productos.</div>";
    return;
  }

  productos.forEach((p) => {
    const card = document.createElement("div");
    card.className = "producto-card";

    const imagenPlaceholder =
      "https://via.placeholder.com/150x150/f2f2f2/999999?text=Sin+Imagen";
    const imagenUrl =
      p.imagenes && p.imagenes.length > 0 ? p.imagenes[0] : imagenPlaceholder;

    // Si el producto viene de la query de categorías tendrá "posicion" de ranking
    // Aprovechamos a dibujar una etiqueta prolija si ese dato está disponible
    const rankingHtml = p.posicion
      ? `<span class="ranking-badge">🏆 #${p.posicion} más vendido</span>`
      : "";

    card.innerHTML = `
            <div class="producto-imagen-wrapper">
                <img src="${imagenUrl}" alt="${p.titulo}" onerror="this.onerror=null; this.src='${imagenPlaceholder}';">
            </div>
            <div class="producto-info">
                <div class="producto-header">
                    ${rankingHtml}
                    <h3 title="${p.titulo}">${p.titulo}</h3>
                    <div class="producto-meta">Marca: <strong>${p.marca || "Genérica"}</strong> | ASIN: <strong>${p.asin}</strong></div>
                    <p class="producto-descripcion">${p.descripcion || "Sin descripción disponible para este producto."}</p>
                </div>
                <div class="producto-footer">
                    <p class="producto-precio">$ ${p.precio ? parseFloat(p.precio).toLocaleString("es-AR") : "N/A"}</p>
                </div>
            </div>
        `;
    contenedor.appendChild(card);
  });
}

function manejarKeyPress(event) {
  if (event.key === "Enter") {
    ejecutarBusqueda();
  }
}
