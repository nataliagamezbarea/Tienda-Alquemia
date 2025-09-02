// Asegurarse de que el DOM se ha cargado completamente antes de ejecutar el código
document.addEventListener('DOMContentLoaded', function() {

  // Escuchar el cambio en el radio button para los colores
  document.querySelectorAll('.color-radio').forEach(function(radio) {
    radio.addEventListener('change', function() {
      // Obtener el id del color seleccionado
      const colorId = this.value;
      const colorNombre = this.getAttribute('data-color-nombre');

      // Actualizar la imagen principal
      updateMainImage(colorId);
    });
  });

  // Función que actualiza la imagen principal con el color seleccionado
  function updateMainImage(colorId) {
    // Verificar si tenemos las imágenes asociadas a ese color
    const images = window.imagenesPorColor[colorId];
    
    if (images && images.length > 0) {
      // Actualizar la imagen principal
      const mainImage = document.getElementById('imagen-principal');
      mainImage.src = images[0];  // Cambiar la imagen principal a la primera imagen del color seleccionado

      // También cambiar las miniaturas
      const miniaturas = document.querySelectorAll('.miniatura');
      miniaturas.forEach((miniatura, index) => {
        if (images[index]) {
          miniatura.src = images[index];  // Actualizar las miniaturas con las imágenes del color
        }
      });
    }
  }

  // Código JS para cambiar la imagen principal al hacer clic en una miniatura
  document.querySelectorAll('.miniatura').forEach(function(miniatura, index) {
    miniatura.addEventListener('click', function() {
      // Cambiar la imagen principal al hacer clic en una miniatura
      const mainImage = document.getElementById('imagen-principal');
      mainImage.src = miniatura.src;
    });
  });

});
