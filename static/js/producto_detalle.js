document.addEventListener('DOMContentLoaded', function() {
  // Obtener el id del producto desde una variable global (renderizada por Flask)
  const productId = window.productId;

  // Obtener las imágenes agrupadas por color para este producto
  const imagesPorColor = window.imagenesPorColor[productId] || {};

  function updateMainImage(colorId) {
    const images = imagesPorColor[colorId];
    if (images && images.length > 0) {
      const mainImage = document.getElementById('imagen-principal');
      mainImage.src = images[0];

      const miniaturas = document.querySelectorAll('.miniatura');
      miniaturas.forEach((miniatura, index) => {
        if (images[index]) {
          miniatura.src = images[index];
          miniatura.style.display = 'block';
        } else {
          miniatura.style.display = 'none';
        }
      });
    }
  }

  // Inicializar con el color seleccionado por defecto (radio checked)
  const checkedRadio = document.querySelector('.color-radio:checked');
  if (checkedRadio) {
    updateMainImage(checkedRadio.value);
  }

  // Escuchar cambios en las opciones de color
  document.querySelectorAll('.color-radio').forEach(radio => {
    radio.addEventListener('change', function() {
      updateMainImage(this.value);
    });
  });

  // Cambiar imagen principal al hacer click en miniatura
  document.querySelectorAll('.miniatura').forEach(miniatura => {
    miniatura.addEventListener('click', () => {
      document.getElementById('imagen-principal').src = miniatura.src;
    });
  });
});
