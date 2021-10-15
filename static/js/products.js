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
        data: {toman_amount: amount}, // serializes the form's elements.
        success: function (data) {
            mecoin = data.mecoin
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

                } else {
                    $('#base-price').html(data.price + unit)
                    $('#mecoin-gift').html(toFarsiNumber(convert_to_mecoin(data.price_with_discount_en)))
                }
            }
        }
    });
}

// short description for product name
function short_description(string) {
    if (string.length > 40) {
        return string.slice(0, 40) + '...'
    } else {
        return string
    }
}

// generate product cart
function product_cart(product) {
    let a;
    let product_detail = $("#product-detail-url").data('url')

    let price;
    if (product.discount_percent_for_api !== null) {

        price = `<div class="d-flex justify-content-end">
                                                    <strike class="card-text m-2"
                                                            style="font-size: 85%">${toFarsiNumber(product.final_price_for_api.toLocaleString())} </strike>
                                                    <p class="p-2"
                                                       style="font-size: 90%; background-color: red; color: white; border-radius: 20px;">${toFarsiNumber(product.discount_percent_for_api)}%</p>
                                                </div>
                                                <p class="card-text">${toFarsiNumber(product.discount_price_for_api.toLocaleString())}
                                                    تومان </p>`
    } else {
        price = `
                 <p class="card-text m-2">${toFarsiNumber(product.discount_price_for_api.toLocaleString())}
                                                    تومان </p>
                `
    }
    a = `
                        <a class="product-a-container" href="${product_detail.replace('0', product.id)}">
                            <div class="card text-right m-3" style="width: 17rem">
                                <div style="height: 15rem;" class="text-center">
                                    <img class="card-img-top" src="${product.first_image}"
                                         style="object-fit: scale-down; height: 100%; width: 100%"
                                         alt="product image">
                                </div>
                                <div class="card-body">
                                    <p class="card-title">${short_description(product.name)}</p>
                                    <div class="text-left price">
                
                                            ${price}
                
                                    </div>
                                </div>
                            </div>
                        </a>
                    
                    `


    return a


}

function pre_next(url, category_id) {

    if (url !== 'null') {
        $.ajax({
            type: "GET",
            url: url,
            success: function (data) {

                let category_div = $(`#cat-${category_id}-product`)
                $(`#next-${category_id}`).attr('onclick', `pre_next('${data.next}', ${category_id})`)
                $(`#pre-${category_id}`).attr('onclick', `pre_next('${data.previous}', ${category_id})`)
                if (data.previous === null) {
                    $(`#pre-${category_id}`).css('color', 'gray')
                }
                else {
                    $(`#pre-${category_id}`).css('color', 'black').hover(function () {
                            $(this).css('cursor', 'pointer')
                        })
                }
                if (data.next === null) {
                    $(`#next-${category_id}`).css('color', 'gray').hover(function () {
                            $(this).css('cursor', 'not-allowed')
                        }, function () {
                            $(this).css('cursor', 'pointer')
                        })
                }
                else {
                    $(`#next-${category_id}`).css('color', 'black').hover(function () {
                            $(this).css('cursor', 'pointer')
                        })
                }
                category_div.html('')
                for (let product of data.results) {
                    category_div.append(product_cart(product))
                }
            }


        });
    }
}

function get_products(category_list, product_id) {
    let url = $("#products-by-category-except-given-id").data('url')
    for (let category of category_list) {
        $.ajax({
            type: "GET",
            url: url + '?category_id=' + category.id + '&product_id=' + product_id,
            success: function (data) {

                let html =
                    `
                        <div class="category-div mt-4 pt-3 pb-3">
                            <div class="row justify-content-between">
                                <div class="col-1" style="margin-top: 5%"> <i class="fa fa-chevron-circle-right button-nav" aria-hidden="true" id="next-${category.id}" style="font-size: 500%" onclick="pre_next('${data.next}', ${category.id})"></i> </div>
                                <div style="height: 28rem" class="col-9 text-center d-flex justify-content-center" id="cat-${category.id}-product"></div>
                                <div class="col-1" style="margin-top: 5%"> <i class="fa fa-chevron-circle-left button-nav" aria-hidden="true" id="pre-${category.id}" style="font-size: 500%" onclick="pre_next('${data.previous}', ${category.id})"></i> </div>
                            </div>
                        </div>    
        `

                if (data.results.length !== 0) {
                    $("#other-products").append(html)
                    if (data.previous === null) {
                        $(`#pre-${category.id}`).css('color', 'gray').hover(function () {
                            $(this).css('cursor', 'not-allowed')
                        }, function () {
                            $(this).css('cursor', 'pointer')
                        })
                    }
                    if (data.next === null) {
                        $(`#next-${category.id}`).css('color', 'gray').hover(function () {
                            $(this).css('cursor', 'not-allowed')
                        }, function () {
                            $(this).css('cursor', 'pointer')
                        })
                    }
                    let category_div = $(`#cat-${category.id}-product`)


                    for (let product of data.results) {

                        category_div.append(product_cart(product))
                    }
                }

            }
        });
    }
}

$(document).ready(function () {

    let category_id = [{id: $("#category-id-data").data('key')}]
    let product_id = $("#product-id-data").data('key')
    console.log(category_id, product_id)
    get_products(category_id, product_id)


})

