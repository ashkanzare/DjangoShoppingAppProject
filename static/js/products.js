// product image slider
var slideIndex = 1;

function plusDivs(n) {
    showDivs(slideIndex += n);
}

function showDivs(n) {
    var i;
    var x = document.getElementsByClassName("mySlides");
    if (n > x.length) {
        slideIndex = 1
    }
    if (n < 1) {
        slideIndex = x.length
    }
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    x[slideIndex - 1].style.display = "block";
}

function get_products_by_category(category_id) {
    event.preventDefault()
    let category_name = $(event.target).html()
    let url = $('#category-products-url').attr('data-url')
    $.ajax({
        type: "POST",
        url: url,
        data: {'category': category_id}, // serializes the form's elements.
        success: function (data) {
            $('#category-modal').modal('toggle');
            $('.modal-title').html(`<p>محصولات مربوط به دسته ی ${category_name}</p>`)
            let products_html = ''
            for (let product of data) {
                products_html += `
                <a href="http://127.0.0.1:8000/product/product-detail/${product.id}">  
                    <div class="d-flex justify-content-between mb-3 p-2" style="border-radius: 15px; background-color: whitesmoke">
                        <div>${product.name.slice(0, 40)}...</div>
                        <div>${product.price}</div>
                    </div>
                </a>  
`
            }
            $('.modal-body').html(products_html)
        }
    });
}

// show all images of the product
function get_product_images(product_id) {
    event.preventDefault()
    let url = $('#products-images-url').attr('data-url')
    $.ajax({
        type: "POST",
        url: url,
        data: {'product_id': product_id}, // serializes the form's elements.
        success: function (data) {
            $('#product-images-modal').modal('toggle');
            let modal_body = $('#product-images-modal-body')
            let images_html = ''
            for (let image of data) {
                console.log(data)
                let img = `<img class="mySlides" src="${image.image}" style="width:100%" alt="product image">`
                images_html += img
            }
            images_html += `
                <div class="text-center mt-4">
                    <button class="w3-button w3-black w3-display-left btn btn-rounded" onclick="plusDivs(-1)">&#10094;</button>
                    <button class="w3-button w3-black w3-display-right btn btn-rounded" onclick="plusDivs(1)">&#10095;</button>
                </div>
            `
            modal_body.html(images_html)
            showDivs(1)
        }
    });
}


// get price impact of chosen property
function get_price_base_of_property(property_id) {
    event.preventDefault()
    let url = $('#product-price-by-property-url').attr('data-url')
    $.ajax({
        type: "POST",
        url: url,
        data: {'property_id': property_id}, // serializes the form's elements.
        success: function (data) {
            if (data !== {}) {
                $('#price').html(data.price)
            }
        }
    });
}

// get price impact of chosen color
function get_price_base_of_color(color_id) {
    event.preventDefault()
    let url = $('#product-price-by-color-url').attr('data-url')
    $.ajax({
        type: "POST",
        url: url,
        data: {'property_id': color_id}, // serializes the form's elements.
        success: function (data) {
            if (data !== {}) {
                $('#price').html(data.price)
            }
        }
    });
}

// deactivate other properties or colors and activate the clicked one
function deactivate(list) {
    for (let data of list) {
        $(data).removeAttr('id')
    }
}

// function for ajax to mecoin api
function convert_to_mecoin(amount) {
    let mecoin_url = $("#convert-toman-to-mecoin-url").attr('data-url')
    let mecoin;
    $.ajax({
        type: "POST",
        async: false,
        url: mecoin_url,
        data: {toman_amount :amount}, // serializes the form's elements.
        success: function (data) {
            mecoin =  data.mecoin
        }
    });
    return mecoin
}

// get price impact of chosen color
function get_price_base_of_color_and_property(property, color, product_id) {
    event.preventDefault()

    deactivate($('.properties'))
    deactivate($('.colors'))
    if (color.length === 0) {
        color = null
    } else {
        $(color).attr('id', 'color-active');
        color = color.data('key')
    }
    if (property.length === 0) {
        property = null
    } else {
        $(property).attr('id', 'property-active');
        property = property.data('key')
    }

    let url = $('#product-price-by-color-and-property-url').attr('data-url')
    $.ajax({
        type: "POST",
        url: url,
        data: {'property_id': property, 'color_id': color, 'product_id': product_id}, // serializes the form's elements.
        success: function (data) {
            let unit = '<span class="m-2 mr-3"\n style="font-size: 70%!important;">تومان</span>'
            if (data !== {}) {
                if (data.price_with_discount !== data.price) {
                    $('#price-with-discount').html(data.price_with_discount + unit)
                    $('#base-price').html(data.price)

                    $('#mecoin-gift').html(toFarsiNumber(convert_to_mecoin(data.price_with_discount_en)))

                }
                else {
                    $('#base-price').html(data.price + unit)
                    $('#mecoin-gift').html(toFarsiNumber(convert_to_mecoin(data.price_with_discount_en)))
                }
            }
        }
    });
}


$(document).ready(function () {

    let url = $('#categories-url').attr('data-url')
    $.ajax({
        type: "GET",
        url: url,
        success: function (data) {
            console.log(data)
            let category_navbar = $('.nav-categories')
            let categories_html = category_navbar.html()
            for (let category of data) {
                categories_html += `
                    <li class="mr-5">
                        <a href="" onclick="get_products_by_category( ${category.id} )">${category.name}</a>
                    </li>
`
            }
            category_navbar.html(categories_html)
        }
    });
    // show first image of the product in slider

    // console.log(111)
    // showDivs(1);

})

