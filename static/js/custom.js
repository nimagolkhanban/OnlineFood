
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
                }else if(response.status == 'Failed'){
                    swal(response.message, '','error')

                } else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);
                    // subtotal, tax and grand total
                     applyCartAmounts(
                         response.cart_amount['subtotal'],
                         response.cart_amount['tax'],
                         response.cart_amount['grand_total'],
                     )
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
                    applyCartAmounts(
                         response.cart_amount['subtotal'],
                         response.cart_amount['tax'],
                         response.cart_amount['grand_total'],
                     )
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
                    applyCartAmounts(
                         response.cart_amount['subtotal'],
                         response.cart_amount['tax'],
                         response.cart_amount['grand_total'],
                     )
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

    // apply cart amounts
    function applyCartAmounts(subtotal, tax, grand_total){
        if(window.location.pathname == '/cart/'){
            $('#subtotal').html(subtotal)
            $('#tax').html(tax)
            $('#total').html(grand_total)
        }

    }

    // $('.add_hour').on('click', function (e){
    //     e.preventDefault();
    //     var day = document.getElementById('id_day').value
    //     var from_hour = document.getElementById('id_from_hour').value
    //     var to_hour = document.getElementById('id_to_hour').value
    //     var is_closed = document.getElementById('id_is_closed').checked
    //     var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
    //     var url = document.getElementById('add_hour_url').checked
    //
    //     console.log(day, from_hour, csrf_token, is_closed, to_hour)
    //     if (is_closed){
    //         is_closed = 'True'
    //         condition = "day != ''"
    //     }else{
    //         is_closed = 'False'
    //         condition = "day != '' && from_hour != '' && to_hour != '' "
    //     }
    //     if (eval(condition)){
    //         $.ajax({
    //             type: 'POST',
    //             url : url,
    //             data : {
    //                 'day':day,
    //                 'from_hour': from_hour,
    //                 'to_hour': to_hour,
    //                 'is_closed':is_closed,
    //                 'csrfmiddlewaretoken': csrf_token,
    //             },
    //             success: function (response){
    //                 console.log(response)
    //             }
    //
    //         })
    //     }else{
    //         swal('please fill all field', '', 'info')
    //     }
    //
    //
    // })
    // document ready close

});
$(document).ready(function() {
    $('.dropdown-toggle').dropdown();
});