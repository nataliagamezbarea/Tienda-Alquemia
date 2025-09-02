document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".opciones-color .color").forEach((colorBtn) => {
    colorBtn.addEventListener("click", function () {
      const targetId = this.dataset.target;
      const colorId = this.dataset.idColor;
      const productoId = targetId.replace("producto-", "");
      const targetDiv = document.getElementById(targetId);

      if (!targetDiv) return;

      fetch(`/producto/${productoId}/color/${colorId}`)
        .then((response) => response.json())
        .then((imagenes) => {
          if (imagenes.length === 0) return;

          const defaultDiv = targetDiv.querySelector(".imagen-producto.default");
          const hoverDiv = targetDiv.querySelector(".imagen-producto.hover");

          if (defaultDiv) defaultDiv.style.backgroundImage = `url('${imagenes[0]}')`;
          if (hoverDiv) hoverDiv.style.backgroundImage = imagenes[1] ? `url('${imagenes[1]}')` : `url('${imagenes[0]}')`;

          // Resaltar color activo
          const colores = document.querySelectorAll(`.opciones-color .color[data-target="${targetId}"]`);
          colores.forEach((btn) => btn.classList.remove("color-activo"));
          this.classList.add("color-activo");
        })
        .catch((err) => console.error(err));
    });
  });
});
