// Función para mostrar el mapa cuando se hace clic en una tienda
function mostrar_mapa(tiendaCard) {
  var mapaUrl = tiendaCard.getAttribute("data-url");

  if (!mapaUrl) {
    console.warn("No se encontró URL de mapa para esta tienda");
    return;
  }

  var iframe = document.getElementById("mapa-maps");
  iframe.src = mapaUrl;
  iframe.style.display = "block";
  document.getElementById("mapa-mensaje").style.display = "none";

  // Scroll suave al mapa
  document.getElementById("mapa").scrollIntoView({ behavior: "smooth" });
}

window.addEventListener("load", function () {
  // Asegurarse de que el iframe está oculto al inicio
  var iframe = document.getElementById("mapa-maps");
  if (iframe) {
    iframe.style.display = "none";
  }
  // Asegurarse de que el mensaje se muestra al inicio
  var mensaje = document.getElementById("mapa-mensaje");
  if (mensaje) {
    mensaje.style.display = "block";
  }
});
