document.addEventListener("DOMContentLoaded", function () {
  const mostrarContrasena = document.getElementById("OjoContraseña");
  const mostrarConfirmarContrasena = document.getElementById("OjoContraseñaConfirmacion");

  function alternarVisibilidad(input, icono) {
    // comparar si el tipo es password cambia a text y si es text a password
    const tipo = input.type === "password" ? "text" : "password";
    //   asignar el tipo
    input.type = tipo;
    //   si esta presente la elimina y si no la añade
    icono.classList.toggle("fa-eye");

    //   si esta presente la elimina y si no la añade
    icono.classList.toggle("fa-eye-slash");
  }

  // mira cuando el usuario hace click
  mostrarContrasena?.addEventListener("click", function () {
    // cambia del id del input y pasa el icono sobre el que se ha pulsado
    alternarVisibilidad(document.getElementById("contrasena"), this);
  });

  mostrarConfirmarContrasena?.addEventListener("click", function () {
    alternarVisibilidad(document.getElementById("confirmar_contrasena"), this);
  });
});
