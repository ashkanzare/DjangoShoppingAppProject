// Create Order
function createOrder() {
    let api_url = $("#create-order-url").data('key')
    let token = $("#user_token").val()
    let cart_id = $("#cart_id").data('key');
    let address_id = $("#selected-address").data('key');
    let shipping_type = $(".selected-shipping")[0].id

    if (shipping_type.includes('meshop')) {
        shipping_type = 'MESHOP'
    }
    else {
        shipping_type = 'POST'
    }

    const data = {
        token: token,
        cart_id: cart_id,
        address_id: address_id,
        shipping_type: shipping_type
    }
    $.ajax({
            type: "POST",
            url: api_url,
            data: data,
            success: function (data) {
                window.location.replace($("#payment-url").data('key'))
            },
            error: function (errors) {
                console.log(errors)
            }
        });

}