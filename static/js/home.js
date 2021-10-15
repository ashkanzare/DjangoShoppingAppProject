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
                } else {
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
                } else {
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

function get_products(category_list) {
    let url = $("#products-by-category-url").data('url')
    for (let category of category_list) {
        $.ajax({
            type: "GET",
            url: url + '?category_id=' + category.id,
            success: function (data) {

                let html =
                    `
                        <div class="category-div mt-4 pt-3 pb-3">
                            <div class="row justify-content-between">
                                <div class="col-1" style="margin-top: 9%"> <i class="fa fa-chevron-circle-right button-nav" aria-hidden="true" id="next-${category.id}" style="font-size: 400%" onclick="pre_next('${data.next}', ${category.id})"></i> </div>
                                <div style="height: 28rem" class="col-9 text-center d-flex justify-content-center" id="cat-${category.id}-product"></div>
                                <div class="col-1" style="margin-top: 9%"> <i class="fa fa-chevron-circle-left button-nav" aria-hidden="true" id="pre-${category.id}" style="font-size: 400%" onclick="pre_next('${data.previous}', ${category.id})"></i> </div>
                            </div>
                        </div>    
        `

                if (data.results.length !== 0) {
                    $("#products-container").append(html)
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

    let category_url = $("#categories-url").data('url')
    $.ajax({
        type: "GET",
        url: category_url,
        success: function (data) {
            get_products(data)
        }
    });

})
