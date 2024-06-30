$(document).ready(function() {
  // INICIO consumo API "http://fakestoreapi.com/products"
  $.get("http://fakestoreapi.com/products", function(data) {
      // Limpiar fila de ropa
      $("#fila-ropa").empty();

      // INICIO $each para recorrer los registros con la ropa
      $.each(data, function(index, item) {
          // Crear string con HTML de un "card de bootstrap" para formatear ropa
          var cardHtml = `
              <div class="col-sm-12 col-md-6 col-lg-4 col-xl-3 mb-3 text-center">
                  <div class="card" style="width: 18rem;">
                      <img src="${item.image}" style="width: 100px; margin: auto;" class="card-img-top pt-3">
                      <div class="card-body">
                          <h5 class="card-title">${item.title}</h5>
                          <p class="card-text">${item.description}</p>
                          <p class="card-text"><strong>Precio: $${item.price}</strong></p>
                                                      <a class="btn btn-primary" target="_blank" href="https://www.amazon.com/s?k=${item.title}">
                                Ver en Amazon
                            </a>
                      </div>
                  </div>
              </div>
          `;

          // Agregar string con el card a fila de ropa
          $("#fila-ropa").append(cardHtml);
      });
      // FIN $each
  });
  // FIN consumo API
});
