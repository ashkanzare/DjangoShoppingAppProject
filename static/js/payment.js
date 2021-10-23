// change icon color
function chang_color(icon_id, input) {
    let credit_card_icon = $('#credit-card-icon')
    let pos_icon = $('#pos-icon')
    let mecoin_icon = $("#mecoin-icon")

    $(input).attr('checked', true)

    if (icon_id === '#credit-card-icon') {
        $("#cash-on-delivery-method input").attr('checked', false)
        $("#mecoin-method input").attr('checked', false)

        credit_card_icon.css('opacity', 1).css('color', '#00BED5FF');
        pos_icon.css('opacity', '0.25').attr("src", "../../static/img/pos.png");
        mecoin_icon.css('opacity', '0.25').attr("src", "../../static/img/mecoin-inactive.png");
    } else if (icon_id === '#mecoin-icon') {
        $("#cash-on-delivery-method input").attr('checked', false)
        $("#online-method input").attr('checked', false)

        credit_card_icon.css('opacity', 0.25).css('color', 'black');
        pos_icon.css('opacity', '0.25').attr("src", "../../static/img/pos.png");
        mecoin_icon.attr("src", "../../static/img/mecoin-active.png").css('opacity', 1);
    } else {
        $("#online-method input").attr('checked', false)
        $("#mecoin-method input").attr('checked', false)

        credit_card_icon.css('opacity', 0.25).css('color', 'black');
        mecoin_icon.css('opacity', '0.25').attr("src", "../../static/img/mecoin-inactive.png");
        pos_icon.attr("src", "../../static/img/pos-active.png").css('opacity', 1);
    }
}

// open discount div
function open_body(div_id, show_div, height) {

    let drop_div = $(div_id + ' .drop-body')
    let drop_button = $(div_id + " .change-height")

    if (drop_div.height() === 5) {
        if (show_div === '#order-summary-drop-down') {
            $(show_div).css('transition', 'all 900ms ease-in')
        }
        drop_button.html('<i class="fa fa-chevron-up" aria-hidden="true"></i>')
        drop_div.css('height', height)
        $(show_div).css('opacity', 1).css('margin-top', '30px')
    } else {
        if (show_div === '#order-summary-drop-down') {
            $(show_div).css('transition', 'all 150ms ease-in')
        }
        drop_button.html('<i class="fa fa-chevron-down" aria-hidden="true"></i>')
        drop_div.css('height', '0.5rem')
        $(show_div).css('opacity', 0).css('margin-top', '0')
    }
}

// enable discount button
function enable_button(elem) {
    $('#discount-errors').html('')
    let button = $(".custom-button")
    if ($(elem).val() !== '') {
        $(elem).css('border', '1px solid rgb(0, 190, 213)')
        button.attr('disabled', false);
    } else {
        $(elem).css('border', '1px solid #ccc')
        button.attr('disabled', true);
    }
}

// check discount
function check_discount() {
    let discount_form_div = $("#discount-form input")
    if (discount_form_div.val() === '') {
        alert('code cant be empty')
    } else {
        let code = discount_form_div.val()
        let token = $("#user-token").data('key')
        let order_id = $("#order-id").data('key')
        let url = $("#check-discount-url").data('key')

        const data = {
            discount_code: code,
            token: token,
            order_id: order_id
        }

        $.ajax({
            type: "POST",
            url: url,
            data: data,
            success: function (data) {

                window.location.reload()
            },
            error: function (err) {
                $("#discount-errors").html(err.responseJSON.error)
                discount_form_div.val('')
            }
        });
    }
}
let a
// confirm order
function confirm_order() {
    let radio_buttons = [
        "#online-method",
        "#mecoin-method",
        "#cash-on-delivery-method"]
    for (let button of radio_buttons) {
        if ($(button + ' input').attr('checked') === 'checked') {
            let radio_index = radio_buttons.indexOf(button)
            if (radio_index === 2) {
                window.location.replace($("#order-cash-on-delivery-url").data('key'))
            }
            else if (radio_index === 1) {
                window.location.replace($("#mecoin-url").data('key'))
            }
        }
    }
}