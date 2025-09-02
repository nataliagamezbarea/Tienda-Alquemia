document.addEventListener("DOMContentLoaded", function () {
  const mainImage = document.getElementById("imagen-principal");
  const miniaturasContainer = document.getElementById("miniaturas");

  // Diccionario de imágenes por color
  const imagesPorColor = window.imagenesPorColor || {};

  function updateImages(colorId) {
    const images = imagesPorColor[colorId] || [];

    // Actualiza imagen principal
    if (mainImage && images.length > 0) mainImage.src = images[0];

    // Actualiza miniaturas
    if (miniaturasContainer) {
      const miniaturas = miniaturasContainer.querySelectorAll(".miniatura");

      miniaturas.forEach((miniatura, index) => {
        if (images[index]) {
          miniatura.src = images[index];
          miniatura.style.display = "block";
        } else {
          miniatura.style.display = "none";
        }
      });
    }
  }

  // Inicializa con el color seleccionado por defecto
  const checkedRadio = document.querySelector(".color-radio:checked");
  if (checkedRadio) updateImages(checkedRadio.value);

  // Cambiar imágenes al seleccionar un color
  document.querySelectorAll(".color-radio").forEach((radio) => {
    radio.addEventListener("change", () => {
      updateImages(radio.value);
    });
  });

  // Cambiar imagen principal al hacer click en miniatura
  if (miniaturasContainer) {
    miniaturasContainer.addEventListener("click", (e) => {
      if (e.target.classList.contains("miniatura")) {
        mainImage.src = e.target.src;
      }
    });
  }
});
