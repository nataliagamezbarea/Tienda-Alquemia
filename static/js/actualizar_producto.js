
    // Función para agregar una variante base (vacía) si no existe ninguna
    function crearVarianteBase() {
        const container = document.getElementById('variantes-container');
        const varianteBase = document.createElement('div');
        varianteBase.classList.add('variante');
        varianteBase.innerHTML = `
            <div class="form-group">
                <a href="javascript:void(0);" onclick="eliminarVariante(0)">
                    <i class="fas fa-trash-alt"></i> Eliminar
                </a>
                <label for="id_color">Color</label>
                <select name="variantes[0][id_color]" required>
                    {% for color in colores %}
                    <option value="{{ color.id_color }}">{{ color.color }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label for="id_talla">Talla</label>
                <select name="variantes[0][id_talla]" required>
                    {% for talla in tallas %}
                    <option value="{{ talla.id_talla }}">{{ talla.talla }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label for="stock">Stock</label>
                <input type="number" name="variantes[0][stock]" required>
            </div>
            <div class="form-group">
                <label for="imagenes">Imágenes para esta variante:</label>
                <div class="imagen-previa">
                    <div>No hay imágenes predeterminadas para esta variante.</div>
                </div>
            </div>
            <div class="form-group">
                <label for="imagenes_nuevas">Agregar nuevas imágenes:</label>
                <input type="file" name="variantes[0][imagenes_nuevas]" accept="image/*" multiple>
            </div>
        `;
        container.appendChild(varianteBase);
    }

    // Función para agregar variantes dinámicamente
    function agregarVariante() {
        const container = document.getElementById('variantes-container');
        
        // Si no existe variante base (template), la creamos
        const varianteBase = document.querySelector('.variante');
        if (!varianteBase) {
            crearVarianteBase();
            return;
        }

        // Clonamos la variante base
        const nuevaVariante = varianteBase.cloneNode(true);
        
        // Actualizamos el índice de la nueva variante
        const nuevaVarianteIndex = container.children.length;
        nuevaVariante.setAttribute('data-variante', nuevaVarianteIndex);

        // Reseteamos los campos de la nueva variante
        nuevaVariante.querySelectorAll('select, input').forEach(field => field.value = "");

        // Añadimos la nueva variante al contenedor
        container.appendChild(nuevaVariante);
    }

    // Función para eliminar una variante
    function eliminarVariante(varianteIndex) {
        const variante = document.querySelector(`[data-variante="${varianteIndex}"]`);
        if (variante) {
            variante.remove();
        }
    }



    // Función para eliminar imagen y actualizar el campo input
function eliminarImagen(varianteIndex, imagenUrl) {
    // Eliminar visualmente la imagen del contenedor
    const variante = document.querySelector(`[data-variante="${varianteIndex}"]`);
    if (variante) {
        const imagenContainers = variante.querySelectorAll('.imagen-container');
        imagenContainers.forEach((container) => {
            if (container.querySelector('img').src.includes(imagenUrl)) {
                // Eliminar la imagen visualmente
                container.remove();
            }
        });

        // Actualizar el valor del input con las URLs restantes
        const inputImagenes = variante.querySelector('input[name^="variantes"][name$="][imagenes_existentes]"]');
        if (inputImagenes) {
            let imagenesExistentes = inputImagenes.value.split(',');

            // Filtramos la URL eliminada
            imagenesExistentes = imagenesExistentes.filter(url => !url.includes(imagenUrl));

            // Actualizamos el valor del input con las imágenes restantes
            inputImagenes.value = imagenesExistentes.join(',');
        }
    }
}


