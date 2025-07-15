document.addEventListener('DOMContentLoaded', function () {
  // Escuchar todos los botones de color con clic
  document.querySelectorAll('.opciones-color .color').forEach(function (colorBtn) {
    colorBtn.addEventListener('click', function () {
      const colorId = this.dataset.idColor;
      const targetId = this.dataset.target;
      const productoId = targetId.replace('producto-', '');

      const targetDiv = document.getElementById(targetId);
      const imagenes = (window.imagenesPorColor?.[productoId]?.[colorId]) || [];

      if (imagenes.length > 0 && targetDiv) {
        const defaultDiv = targetDiv.querySelector('.imagen-producto.default');
        const hoverDiv = targetDiv.querySelector('.imagen-producto.hover');

        if (defaultDiv) {
          defaultDiv.style.backgroundImage = `url('${imagenes[0]}')`;
        }

        if (hoverDiv) {
          hoverDiv.style.backgroundImage = imagenes[1]
            ? `url('${imagenes[1]}')`
            : `url('${imagenes[0]}')`; // fallback a la imagen principal si no hay segunda
        }
      }

      // Opcional: resaltar el color activo, removiendo antes de todos los colores de ese producto
      const colores = document.querySelectorAll(`.opciones-color .color[data-target="${targetId}"]`);
      colores.forEach(btn => btn.classList.remove('color-activo'));
      this.classList.add('color-activo');
    });
  });
});
