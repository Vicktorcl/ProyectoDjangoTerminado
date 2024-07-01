$(document).ready(function() {
    // BOTON IMAGEN: Prepara el botón de  
      // 1. Ocultar la etiqueta que acompaña al botón de "Seleccionar archivo" (el clásico botón input type file)
      // 2. Mueve el botón de "Seleccionar archivo" debajo del "cuadro_imagen" que es el "img" que muestra la foto
      // 3. Oculta parcialmente el botón de "Seleccionar archivo", así el error de jquery validate 
      //    se mostrará debajo de la imagen cuando el usuario no haya seleccionado alguna.
      // 4. En la página que usa el botón de "Seleccionar archivo" se debe poner otro en su reemplazo
      if ($('#id_imagen').length > 0) {
        $("label[for='id_imagen']").hide();
        $('#id_imagen').insertAfter('#cuadro-imagen');
        $("#id_imagen").css("opacity", "0");
        $("#id_imagen").css("height", "0px");
        $("#id_imagen").css("width", "0px");
        $('#form').removeAttr('style');
      }
    
        // BOTON DE SELECCIONAR IMAGEN: Cuando se selecciona una nueva imagen usando el botón,
      // entonces se carga la imagen en el tag "img" que tiene el id "cuadro-imagen" 
      if ($('#id_imagen').length > 0) {
        $('#id_imagen').change(function() {
          var input = this;
          if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
              $('#cuadro-imagen').attr('src', e.target.result).show();
            };
            reader.readAsDataURL(input.files[0]);
          }
        });
      }
    
    });