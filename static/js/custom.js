
$(document).ready(function(){
    // add to cart
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        $.ajax({
            typ: 'GET',
            url: url,
            success: function(response){
                console.log(response.cart_counter['cart_count'])
                 if(response.status == 'Failed'){
                    console.log(response)
                }
                else{
                   $('#cart_counter').html(response.cart_counter['cart_count']);
                $('#qty-'+food_id).html(response.qty);
            }
            }
        })
    })

    // places the quantity in the page dynamically
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
    })

    // decrease cart
    $('.decrease_cart').on('click', function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        $.ajax({
            typ: 'GET',
            url: url,
            success: function(response){
                console.log(response.cart_counter['cart_count'])
                if(response.status == 'Failed'){
                    console.log(response)
                }
                else{
                   $('#cart_counter').html(response.cart_counter['cart_count']);
                $('#qty-'+food_id).html(response.qty);
            }
                }
        })
    })
});
