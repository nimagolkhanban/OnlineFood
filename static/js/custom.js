
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
                console.log(response)
                 if(response.status == 'login_required'){
                    swal(response.message, '','info').then(function(){
                        window.location = '/accounts/login/';
                    })
                }
                 if(response.status == 'Failed'){
                    swal(response.message, '','error')

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
        cart_id = $(this).attr('id');

        $.ajax({
            typ: 'GET',
            url: url,
            success: function(response){
                console.log(response)
                if(response.status == 'login_required'){
                    swal(response.message, '','info').then(function(){
                        window.location = '/accounts/login/';
                    })
                }else if(response.status == 'Failed'){
                    swal(response.message, '','error')
                } else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);
                    if (window.location.pathname == '/cart/'){
                        removeCartItem(response.qty, cart_id);
                        checkEmptyCart();
                    }
                }
            }
        })
    })

    $('.delete_cart').on('click', function(e){
        e.preventDefault();

        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        $.ajax({
            typ: 'GET',
            url: url,
            success: function(response){
                console.log(response)

                if(response.status == 'Failed'){
                    swal(response.message, '','error')
                } else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    swal(response.status, response.message, 'success')
                    removeCartItem(0, cart_id);
                    checkEmptyCart();
                }
            }
        })
    })
    // delete item from cart
    function removeCartItem(cartItemQty, cart_id){
        if(cartItemQty <=0){
            // remove the cart item element
            document.getElementById("cart-item-"+cart_id).remove()
        }
    }
    // check if the cart is empty to show the message
    function checkEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if (cart_counter == 0){
            document.getElementById("empty-cart").style.display = "block";
        }
    }

});
