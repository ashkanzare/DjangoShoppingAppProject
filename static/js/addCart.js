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

// get cart-counter for cart icon in navbar
function get_cart() {
    let cart = 'cart_counter'
    let local_storage_cart = localStorage.getItem(cart)
    let cart_counter = $('#cart-counter')
    if (local_storage_cart) {

        cart_counter.html(toFarsiNumber(local_storage_cart))

        if (Number(local_storage_cart) === 0) {
            cart_counter.css('visibility', 'hidden')
        }
        return local_storage_cart

    } else {

        cart_counter.html(local_storage_cart).css('visibility', 'hidden')
        return null
    }

}

// add local storage cart items to current active cart
function add_from_local_to_server(token) {
    localStorage.removeItem('cart_counter')
    let session = localStorage.getItem('session')
    localStorage.removeItem('session')
    let url = $('#sync-carts-url').data('url')

    $.ajax({
        type: "POST",
        url: url,
        data: {'token': token, 'session': session}, // serializes the form's elements.
        success: function (data) {
            console.log(data)
        }
    });


}

// set null if undefined
function set_null(obj) {
    if (obj === undefined) {
        return null
    } else {
        return obj
    }
}


function add_cart_to_database(token, product, color_id = null, property_id = null, item_id = null, number = null) {
    let delete_all = false
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
    } else if (number === 'delete_all') {
        number = -Number(convert_fa_to_en($(`#item-${item_id}`).html()))
        data.number = number
        delete_all = true
    }

    console.log(data)
    $.ajax({
        type: "POST",
        url: url,
        data: data, // serializes the form's elements.
        success: function (data) {
            localStorage.setItem('cart_counter', data.cart_count)
            localStorage.setItem('session', data.session)
            if (data.cart_count !== 0) {
                $('#cart-counter').html(toFarsiNumber(data.cart_count)).css('visibility', 'visible')
            } else {
                $('#cart-counter').html(data.cart_count).css('visibility', 'hidden')
            }
            if (data.status === 30) {
                alert('متاسفانه امکان انتخاب بیشتر موجود نیست')
            } else {
                // update cart price div
                let cart_price_with_discount = $('#cart-price-without-discount')
                let cart_discount = $('#cart-discount')
                let cart_total_price = $('#cart-total-price')

                cart_price_with_discount.html(`<h5>${toFarsiNumber(data.cart[0].toLocaleString())}</h5>`)
                cart_discount.html(` <h5 class="text-danger d-flex justify-content-end">
                                        <span class="ml-2">(${toFarsiNumber(data.cart[2].toLocaleString())}%)  </span><span>${toFarsiNumber(data.cart[3].toLocaleString())}</span>
                                    </h5>`)
                cart_total_price.html(`<h5>${toFarsiNumber(data.cart[1].toLocaleString())}</h5>`)


                let item_number = $('#item-' + item_id)
                let en_number = Number(convert_fa_to_en(item_number.html()))
                if (number > 0) {
                    item_number.html(toFarsiNumber(en_number + 1))
                    let item_discount = $('#discount-per-items')
                    let item_price = $('#price-per-items')

                    $('#discount-price-value').html(toFarsiNumber((item_discount.data('key') * (en_number + 1)).toLocaleString()))
                    $('#price-value').html(toFarsiNumber((item_price.data('key') * (en_number + 1)).toLocaleString()))

                    get_cart()
                } else {
                    if (delete_all) {
                        item_number.html('۰')

                        let cart_reserve_info = $('#cart-reserve-info')
                        cart_reserve_info.animate({opacity: 0}, 100,)
                        setTimeout(function () {
                            cart_reserve_info.remove()
                        }, 300);
                    } else {
                        item_number.html(toFarsiNumber(en_number - 1))
                        let item_discount = $('#discount-per-items')
                        let item_price = $('#price-per-items')

                        $('#discount-price-value').html(toFarsiNumber((item_discount.data('key') * (en_number - 1)).toLocaleString()))
                        $('#price-value').html(toFarsiNumber((item_price.data('key') * (en_number - 1)).toLocaleString()))
                    }
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
                    $("#cart-price-div").remove()

                }
            }, 300);


        }
    });


}


function show_cart_from_local() {
    let cart = 'meshop'
    let local_storage_cart = localStorage.getItem(cart)
    if (local_storage_cart) {

        let url = $('#cart-items-for-local').data('url')
        let cart_obj = JSON.parse(local_storage_cart)
        $.ajax({
            type: "POST",
            url: url,
            data: cart_obj, // serializes the form's elements.
            success: function (data) {
                console.log(cart_obj)
            }
        });


    }
}
