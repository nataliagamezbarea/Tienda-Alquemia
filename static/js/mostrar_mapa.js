// Función para mostrar el mapa cuando se hace clic en una tienda
function mostrar_mapa(tiendaCard) {
  var mapaUrl = tiendaCard.getAttribute("data-url");

  var iframe = document.getElementById("mapa-maps");
  iframe.src = mapaUrl;
  iframe.style.display = "block"; // Mostrar el iframe
  document.getElementById("mapa-mensaje").style.display = "none"; // Ocultar el mensaje de búsqueda
}

window.onload = function () {
  // Asegurarse de que el iframe está oculto al inicio
  var iframe = document.getElementById("mapa-maps");
  iframe.style.display = "none";
  // Asegurarse de que el mensaje se muestra al inicio
  document.getElementById("mapa-mensaje").style.display = "block";
};
