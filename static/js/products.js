let a;

function get_products_by_category(category_id) {
    event.preventDefault()
    let category_name = $(event.target).html()
    let url = $('#category-products-url').attr('data-url')
    $.ajax({
        type: "POST",
        url: url,
        data: {'category': category_id}, // serializes the form's elements.
        success: function (data) {
            console.log(data)
            $('#category-modal').modal('toggle');
            $('.modal-title').html(`<p>محصولات مربوط به دسته ی ${category_name}</p>`)
            let products_html = ''
            for (let product of data) {
                products_html += `
                    <div class="d-flex justify-content-between mb-3 p-2" style="border-radius: 15px; background-color: whitesmoke">
                        <div>${product.name.slice(0, 40)}...</div>
                        <div>${product.price}</div>
                    </div>
`
            }
            $('.modal-body').html(products_html)
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

})

