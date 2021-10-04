//convert persian numbers to english
function convert_fa_to_en(str) {
    return str.replace(/([۰-۹])/g, function (token) {
        return String.fromCharCode(token.charCodeAt(0) - 1728);
    });
}

//convert english numbers to persian
function toFarsiNumber(n) {
    const farsiDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];

    return n
        .toString()
        .replace(/\d/g, x => farsiDigits[x]);
}

// get cart from local storage
function get_cart() {
    let cart = 'meshop'
    let local_storage_cart = localStorage.getItem(cart)
    if (local_storage_cart) {
        let cart_obj = JSON.parse(local_storage_cart)
        let cart_length = Object.keys(cart_obj).length

        $('#cart-counter').html(cart_length).css('visibility', 'visible')
        return {
            'cart': cart_obj,
            'cart_length': cart_length
        }
    }
    $("#cart-counter").css('visibility', 'hidden')
    return null

}


// add local storage cart items to current active cart
function add_from_local_to_server(token) {
    let cart = 'meshop'
    let local_storage_cart = localStorage.getItem(cart)
    if (local_storage_cart) {
        let url = $('#add-to-cart-url').data('url')
        let cart_obj = JSON.parse(local_storage_cart)

        for (let obj of cart_obj) {
            $.ajax({
                type: "POST",
                url: url,
                data: Object.assign({'token': token}, obj), // serializes the form's elements.
                success: function (data) {
                    console.log(data)
                    $('#cart-counter').html(data.cart_count)
                }
            });
        }
        localStorage.removeItem(cart)
    }
}

// set null if undefined
function set_null(obj) {
    if (obj === undefined) {
        return null
    } else {
        return obj
    }
}

// add to local storage
function add_to_cart_on_local(product) {
    let cart = 'meshop'
    let local_storage_cart = localStorage.getItem(cart)
    if (local_storage_cart) {
        let cart_obj = JSON.parse(local_storage_cart)
        let new_product = {
            'product': product,
            'product_color': set_null($('#color-active').data('key')),
            'product_property': set_null($('#property-active').data('key')),
            'number': 1
        }
        let check = false;
        for (let obj of cart_obj) {
            if (new_product.product === obj.product && new_product.product_color === obj.product_color && new_product.product_property === obj.product_property) {
                obj.number += 1
                check = true
            }
        }
        if (check === false) {
            cart_obj.push(new_product)
        }
        localStorage.setItem(cart, JSON.stringify(cart_obj))
    } else {
        let cart_obj = [{
            'product': product,
            'product_color': set_null($('#color-active').data('key')),
            'product_property': set_null($('#property-active').data('key')),
            'number': 1
        }]
        localStorage.setItem(cart, JSON.stringify(cart_obj))
    }

    get_cart()
}


function add_cart_to_database(token, product, color_id = null, property_id = null, item_id = null, number = null) {

    let url = $('#add-to-cart-url').data('url')
    const data = {
        'token': token,
        'product': product,
        'product_color': set_null($('#color-active').data('key')),
        'product_property': set_null($('#property-active').data('key')),
        'number': 1
    }
    if (color_id) {
        data.product_color = color_id
    }

    if (property_id) {
        data.product_property = property_id
    }

    if (number < 0) {
        data.number = number
    }

    console.log(data)
    $.ajax({
        type: "POST",
        url: url,
        data: data, // serializes the form's elements.
        success: function (data) {
            console.log(data)
            $('#cart-counter').html(data.cart_count)
            if (data.status === 30) {
                alert('متاسفانه امکان انتخاب بیشتر موجود نیست')
            } else {

                // update cart price div
                let cart_price_with_discount = $('#cart-price-without-discount')
                let cart_discount = $('#cart-discount')
                let cart_total_price = $('#cart-total-price')

                cart_price_with_discount.html(data.cart[0])
                cart_discount.html(data.cart[2])
                cart_total_price.html(data.cart[1])


                let item_number = $('#item-' + item_id)
                let en_number = Number(convert_fa_to_en(item_number.html()))
                if (number > 0) {
                    item_number.html(toFarsiNumber(en_number + 1))
                } else {
                    item_number.html(toFarsiNumber(en_number - 1))
                }
                if (item_number.html() === '۰' && number < 0) {
                    let item_element = $('#item-container-' + item_id)
                    item_element.animate({opacity: 0}, 100,)
                    setTimeout(function () {
                        item_element.remove()
                    }, 300);
                }

            }
            setTimeout(function () {
                let cart_main_div = $('#main-cart-body')
                if (cart_main_div.children().length === 0) {
                    let empty_div = `
                                    <div class="text-center p-5">
                                        <img class="cart-image" src="${$('#empty-cart-img').data('key')}" alt="empty-cart">
                                        <h4>سبد خرید شما خالی است!</h4>
                                    </div>                                                                                
`
                    cart_main_div.html(empty_div)

                }
            }, 300);


        }
    });


}