// static/js/carrito.js
$(document).ready(function() {
    $('.delete-icon').on('click', function() {
        const itemId = $(this).data('id');
        $.post('/eliminar-del-carro', { idcan: itemId }, function(data) {
            alert(data.message || "Canción eliminada del carro.");
            location.reload(); // Recargar la página para actualizar el carrito visualmente
        });
    });

    $('.add-to-cart').on('click', function() {
        const idcan = $(this).data('id');
        const titulocan = $(this).data('titulo');
        const preciocan = $(this).data('precio');

        $.post('/agregar-al-carro', {
            idcan: idcan,
            titulocan: titulocan,
            preciocan: preciocan
        }, function(data) {
            alert(data.message || "Canción agregada al carro.");
        });
    });
});



