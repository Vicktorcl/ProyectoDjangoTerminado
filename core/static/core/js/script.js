$(document).ready(function() {

  $('[data-toggle="tooltip"]').tooltip();

  // TABLA AVANZADA: Si hay una tabla con el id "tabla-principal", la transformará en "DataTable Avanzada"
  // Ver sitio web https://datatables.net/
  if ($('#tabla-principal').length > 0) {
    var table = new DataTable('#tabla-principal', {
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json',
        },
    });
  }

  // BOTON LIMPIAR FORMULARIO: Permite limpiar el formulario y las validaciones en rojo si las hubiera
  if ($('#limpiar_formulario').length > 0) {
    $('#limpiar_formulario').click(function(event) {
      $("#form").validate().resetForm();
    });
  }

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

  // CHECKBOX SUBSCRITO: Cambiar la gráfica del checkbox de "subscrito" para agregarle un texto de ayuda
  if ($('#id_subscrito').length > 0) {
    $('#id_subscrito').wrap('<div class="row"></div>');
    $('#id_subscrito').wrap('<div class="col-sm-1" id="checkbox-subscrito"></div>');
    $('#checkbox-subscrito').after('<div id="help_text_id_subscrito" class="col-sm-11"></div>');
    $('#help_text_id_subscrito').text(`Deseo subscribirme con un aporte
      de $3.000 mensuales a la fundación "Help a Brother" y obtner un 
      5% de descuento en todas mis compras.`);
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

  // ACTIVAR CARRUSEL
  if ($('#carousel-indicators').length > 0) {
    const myCarouselElement = document.querySelector('#carousel-indicators');
    const carousel = new bootstrap.Carousel(myCarouselElement, {
      interval: 10,
      touch: false
    });
  };

  // AGREGAR METODO DE VALIDACION PARA EL RUT (ROL UNICO TRIBUTARIO) DE CHILE
  $.validator.addMethod("rutChileno", function(value, element) {
    // Eliminar puntos y guión del RUT
    value = value.replace(/[.-]/g, "");

    // Validar que el RUT tenga 8 o 9 dígitos
    if (value.length < 8 || value.length > 9) {
      return false;
    }

    // Validar que el último dígito sea un número o una 'K'
    var validChars = "0123456789K";
    var lastChar = value.charAt(value.length - 1).toUpperCase();
    if (validChars.indexOf(lastChar) == -1) {
      return false;
    }

    // Calcular el dígito verificador
    var rut = parseInt(value.slice(0, -1), 10);
    var factor = 2;
    var sum = 0;
    var digit;
    while (rut > 0) {
      digit = rut % 10;
      sum += digit * factor;
      rut = Math.floor(rut / 10);
      factor = factor === 7 ? 2 : factor + 1;
    }
    var dv = 11 - (sum % 11);
    dv = dv === 11 ? "0" : dv === 10 ? "K" : dv.toString();

    // Validar que el dígito verificador sea correcto
    return dv === lastChar;
  }, "Por favor ingrese un RUT válido.");

    // Obliga a que la caja de texto del rut, siempre escriba la letra "K" en mayúscula y elimine los puntos
    if(document.getElementById('id_rut')){
      document.getElementById('id_rut').addEventListener('keyup', function(e) {
        e.target.value = e.target.value.toUpperCase();
        for (let i = 0; i < e.target.value.length; i++) {
          const caracter = e.target.value[i];
          if (!"0123456789kK-".includes(caracter)) {
            e.target.value = e.target.value.replace(caracter, "");
          }
        }
      });
    }

    // Agregar método de validación para correo
    $.validator.addMethod("emailCompleto", function(value, element) {

      // Expresión regular para validar correo electrónico
      var regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z\-0-9]{2,}))$/;

      // Validar correo electrónico con la expresión regular
      return regex.test(value);

    }, 'El formato del correo no es válido');
    
    // Agregar método de validación para que un campo sólo acepte 
    // letras y espacios en blanco, pero no números ni símbolos,
    // ideal para campos como nombres y apellidos
    $.validator.addMethod("soloLetras", function(value, element) {

      return this.optional(element) || /^[a-zA-Z\s]*$/.test(value);

    }, "Sólo se permiten letras y espacios en blanco.");

  // AGREGAR METODO DE VALIDACION PARA REVISAR SI UN VALOR SE ENCUENTRA DENTRO DE UNA LISTA DEFINIDA
  // POR EJEMPLO PARA REVISAR SI EL TIPO DE USUARIO ESTÁ DENTRO DE LA LISTA ['Administrador', 'Superusuario']
  $.validator.addMethod("inList", function(value, element, param) {
    return $.inArray(value, param) !== -1;
  }, "Por favor, selecciona un valor válido.");

});
