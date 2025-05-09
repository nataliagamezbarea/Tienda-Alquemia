document.addEventListener("DOMContentLoaded", function () {
  // Filtrar tiendas según las opciones seleccionadas
  function filtrarTiendas() {
    // Obtener los valores seleccionados de los filtros
    var paisSeleccionado = document.getElementById("select-pais").value;
    var provinciaSeleccionada =
      document.getElementById("select-provincia").value;
    var ciudadSeleccionada = document.getElementById("select-ciudad").value;

    // Obtener todas las tarjetas de tiendas
    var tiendas = document.querySelectorAll(".tienda-card");

    // Recorrer todas las tarjetas de tiendas
    tiendas.forEach(function (tienda) {
      // Obtener los datos de cada tienda (país, provincia, ciudad)
      var paisTienda = tienda.getAttribute("data-pais");
      var provinciaTienda = tienda.getAttribute("data-provincia");
      var ciudadTienda = tienda.getAttribute("data-ciudad");

      // Verificar si la tienda debe mostrarse (coincide con los filtros seleccionados)
      var mostrarTienda = true; // Asumimos que se debe mostrar

      // Comprobar si la tienda coincide con los filtros
      if (paisSeleccionado && paisTienda !== paisSeleccionado) {
        mostrarTienda = false;
      }
      if (provinciaSeleccionada && provinciaTienda !== provinciaSeleccionada) {
        mostrarTienda = false;
      }
      if (ciudadSeleccionada && ciudadTienda !== ciudadSeleccionada) {
        mostrarTienda = false;
      }

      // Mostrar u ocultar la tienda según si coincide con los filtros
      if (mostrarTienda) {
        tienda.style.display = "block"; // Mostrar la tienda
      } else {
        tienda.style.display = "none"; // Ocultar la tienda
      }
    });
  }

  // Asociar el evento de cambio a los filtros (selectores)
  document
    .getElementById("select-pais")
    .addEventListener("change", filtrarTiendas);
  document
    .getElementById("select-provincia")
    .addEventListener("change", filtrarTiendas);
  document
    .getElementById("select-ciudad")
    .addEventListener("change", filtrarTiendas);

  // Llamar a la función de filtrado al cargar la página
  filtrarTiendas();
});
