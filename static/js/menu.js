  function mostrarGenero(genero) {
    document.querySelectorAll('.genero').forEach(g => g.classList.add('hidden'));
    document.getElementById(genero).classList.remove('hidden');

    document.querySelectorAll('#sugerencias_genero button').forEach(btn => {
      btn.classList.remove('underline');
    });

    const botones = {
      menu_mujer: 'MUJER',
      menu_hombre: 'HOMBRE'
    };
    document.querySelectorAll('#sugerencias_genero button').forEach(btn => {
      if (btn.textContent.trim() === botones[genero]) {
        btn.classList.add('underline');
      }
    });
  }
