function get_products_by_category(category_id) {
    event.preventDefault()
    let url = $('#category-products-url').attr('data-url')
    $.ajax({
        type: "POST",
        url: url,
        data: {'category': category_id}, // serializes the form's elements.
        success: function (data) {
            console.log(data)
            $('#category-modal').modal('toggle');
            $('.modal-title').html(`<p>محصولات مربوط به دسته ی ${data[0].category.name}</p>`)
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
