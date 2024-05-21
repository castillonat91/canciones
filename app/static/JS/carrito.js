$(document).ready(function(){
    $('.add-to-cart').on('click',function(){
        const idcan = $(this).data('id');
        const titulocan = $(this).data('titulo');
        const preciocan = $(this).data('precio');

        $.post('/agregar-al-carro',{
            idcan:idcan,
            titulocan:titulocan,
            preciocan:preciocan
        },function(data){
            alert(data.message || " agregada cancion al carro.");
        });
    });
});