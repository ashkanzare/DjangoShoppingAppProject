// change icon color
function chang_color(icon_id) {
    let credit_card_icon = $('#credit-card-icon')
    let pos_icon = $('#pos-icon')

    if (icon_id === '#credit-card-icon') {
        credit_card_icon.css('opacity', 1).css('color', '#00BED5FF')
        pos_icon.css('opacity', '0.25').attr("src", "../../static/img/pos.png")
    } else {
        credit_card_icon.css('opacity', 0.25).css('color', 'black')
        pos_icon.attr("src", "../../static/img/pos-active.png").css('opacity', 1);
    }
}

// open discount div
function open_body(div_id, show_div, height) {

    let drop_div = $(div_id + ' .drop-body')
    console.log(drop_div)
    let drop_button = $(div_id + " .change-height")
    console.log(drop_button)

    if (drop_div.height() === 5) {
        if (show_div === '#order-summary') {
            $(show_div).css('transition', 'all 900ms ease-in')
        }
        drop_button.html('<i class="fa fa-chevron-up" aria-hidden="true"></i>')
        drop_div.css('height', height)
        $(show_div).css('opacity', 1).css('margin-top', '30px')
    }
    else {
        if (show_div === '#order-summary') {
            $(show_div).css('transition', 'all 150ms ease-in')
        }
        drop_button.html('<i class="fa fa-chevron-down" aria-hidden="true"></i>')
        drop_div.css('height', '0.5rem')
        $(show_div).css('opacity', 0).css('margin-top', '0')
    }
}

// enable discount button
function enable_button(elem) {
    let button = $(".custom-button")
    if ($(elem).val() !== '') {
        $(elem).css('border', '1px solid rgb(0, 190, 213)')
        button.attr('disabled', false);
    }
    else {
        $(elem).css('border', '1px solid #ccc')
        button.attr('disabled', true);
    }
}

// check discount
function check_discount() {
    let discount_form_div = $("#discount-form")
    if (discount_form_div.val() === '') {
        alert('code cant be empty')
    }
}