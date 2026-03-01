document.addEventListener("DOMContentLoaded", function () {
  // Esperar a que el DOM esté completamente listo
  setTimeout(function() {
    initializarFiltros();
  }, 100);
});

function initializarFiltros() {
  // Obtener datos de tiendas desde el DOM (del template Jinja2)
  const tiendas = document.querySelectorAll(".tienda-card");
  
  if (tiendas.length === 0) {
    console.warn("No tiendas encontradas en el DOM");
    return;
  }

  const tiendaData = Array.from(tiendas).map(tienda => ({
    element: tienda,
    pais: tienda.getAttribute("data-pais"),
    provincia: tienda.getAttribute("data-provincia"),
    ciudad: tienda.getAttribute("data-ciudad")
  }));

  console.log("Tiendas cargadas:", tiendaData.length);

  // Selects
  const selectPais = document.getElementById("select-pais");
  const selectProvincia = document.getElementById("select-provincia");
  const selectCiudad = document.getElementById("select-ciudad");

  if (!selectPais || !selectProvincia || !selectCiudad) {
    console.error("Selects no encontrados en el DOM");
    return;
  }

  // Función para obtener países únicos y ordenados
  function obtenerPaises() {
    const paises = new Set();
    tiendaData.forEach(tienda => {
      if (tienda.pais) {
        paises.add(tienda.pais);
      }
    });
    return Array.from(paises).sort();
  }

  // Función para actualizar las opciones de provincia según el país seleccionado
  function actualizarProvincias() {
    const paisSeleccionado = selectPais.value;
    const provinciasDisponibles = new Set();

    tiendaData.forEach(tienda => {
      if (!paisSeleccionado || tienda.pais === paisSeleccionado) {
        if (tienda.provincia) {
          provinciasDisponibles.add(tienda.provincia);
        }
      }
    });

    // Limpiar y repoblar el select de provincias
    selectProvincia.innerHTML = '<option value="">Seleccionar Provincia</option>';
    Array.from(provinciasDisponibles).sort().forEach(provincia => {
      const option = document.createElement("option");
      option.value = provincia;
      option.textContent = provincia;
      selectProvincia.appendChild(option);
    });

    // Reset ciudad cuando cambia país
    selectCiudad.value = "";
    actualizarCiudades();
  }

  // Función para actualizar las opciones de ciudad según país y provincia
  function actualizarCiudades() {
    const paisSeleccionado = selectPais.value;
    const provinciaSeleccionada = selectProvincia.value;
    const ciudadesDisponibles = new Set();

    tiendaData.forEach(tienda => {
      const paisCoinc = !paisSeleccionado || tienda.pais === paisSeleccionado;
      const provinciaCoinc = !provinciaSeleccionada || tienda.provincia === provinciaSeleccionada;

      if (paisCoinc && provinciaCoinc && tienda.ciudad) {
        ciudadesDisponibles.add(tienda.ciudad);
      }
    });

    // Limpiar y repoblar el select de ciudades
    selectCiudad.innerHTML = '<option value="">Seleccionar Ciudad</option>';
    Array.from(ciudadesDisponibles).sort().forEach(ciudad => {
      const option = document.createElement("option");
      option.value = ciudad;
      option.textContent = ciudad;
      selectCiudad.appendChild(option);
    });
  }

  // Función para filtrar tiendas según los criterios seleccionados
  function filtrarTiendas() {
    const paisSeleccionado = selectPais.value;
    const provinciaSeleccionada = selectProvincia.value;
    const ciudadSeleccionada = selectCiudad.value;

    let tiendaVisiblesCount = 0;
    tiendaData.forEach(tienda => {
      const paisCoinc = !paisSeleccionado || tienda.pais === paisSeleccionado;
      const provinciaCoinc = !provinciaSeleccionada || tienda.provincia === provinciaSeleccionada;
      const ciudadCoinc = !ciudadSeleccionada || tienda.ciudad === ciudadSeleccionada;

      if (paisCoinc && provinciaCoinc && ciudadCoinc) {
        tienda.element.style.display = "block";
        tiendaVisiblesCount++;
      } else {
        tienda.element.style.display = "none";
      }
    });

    console.log("Tiendas visibles:", tiendaVisiblesCount);
  }

  // Eventos de cambio
  selectPais.addEventListener("change", () => {
    actualizarProvincias();
    filtrarTiendas();
  });

  selectProvincia.addEventListener("change", () => {
    actualizarCiudades();
    filtrarTiendas();
  });

  selectCiudad.addEventListener("change", () => {
    filtrarTiendas();
  });

  // Inicializar selects con datos
  console.log("Inicializando filtros...");
  actualizarProvincias();
}
