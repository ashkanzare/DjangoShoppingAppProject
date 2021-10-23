function refresh_code(token) {
    let url = $('#customer-refresh-code-url').attr('data-url')
    $.ajax({
        type: "POST",
        url: url,
        data: {'token': token},
        success: function (data) {
            if (data['status'] === 20) {
                console.log('yes')
            } else {
                console.log('no')
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
    $.ajax({
        type: "POST",
        url: $("#product-image-url").data('url'),
        data: {product_id: product.id},
        async: false,
        success: function (data) {
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
                                    <img class="card-img-top" src="${data[0].image}"
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

        }


    });
    return a


}


$(document).ready(function () {

    $('#category-icon').hover(function () {
        $('#category-div').css('display', 'block')
    }, function () {
        $('#category-div').hover(function () {
            $('#category-div').css('display', 'block')
        }, function () {
            $('#category-div').css('display', 'none');
            $("#navbar-title").hover(function () {
                $('#category-div').css('display', 'none');
            })
        })
    })


    window.onscroll = function () {
        scrollFunction()
    };

    function scrollFunction() {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            if (document.getElementById("under-nav-bar")) {
                document.getElementById("under-nav-bar").style.top = "-50px";
            }
        } else {
            if (document.getElementById("under-nav-bar")) {
                document.getElementById("under-nav-bar").style.top = "0";
            }
        }
    }

    // refresh code ajax
    if (document.referrer.includes('customer/register-login/')) {
        if (performance.navigation.type === performance.navigation.TYPE_RELOAD) {
            refresh_code(window.location.href.split(`?`)[1].substring(6,).split('&')[0])
        }
    } else if (window.location.href.includes('token') && window.location.href.includes('login_type=onetime_code') || window.location.href.includes('register/confirm?token') || window.location.href.includes('confirm-code-reset-password')) {
        refresh_code(window.location.href.split(`?`)[1].substring(6,).split('&')[0])
    } else if (performance.navigation.type === performance.navigation.TYPE_RELOAD && !(window.location.href.includes('token', 'login_type=password'))) {
        if (window.location.href.split(`?`)[1] !== undefined) {
            refresh_code(window.location.href.split(`?`)[1].substring(6,).split('&')[0])
        }
    }


    // reset password phone
    $("#reset-password-form").submit(function (e) {
        e.preventDefault(); // avoid to execute the actual submit of the form.

        let form = $(this);
        let url = form.attr('action');

        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(), // serializes the form's elements.
            success: function (data) {
                if (data['status'] === 0) {
                    let new_url = $("#customer-check-code-reset-password-url").attr('data-url') + "?token=" + data['token'];
                    window.location.replace(new_url)
                } else if (data['status'] === 2) {
                    $('#ajax-errors').html('<p style=\'font-size: 70%!important;\'>درخواست شما با خطا مواجه شد لطفا صفحه را مجدد بارگذاری کنید</p>')
                    message_pop_up()
                } else if (data['status'] === 3) {
                    let parent = $('.jumbotron')
                    let email_message_info = `
                    <div class="container text-center d-flex justify-content-center popup">
                  
                            <div class="panel text-right w-50 auth-panel p-4">
                                <div class="text-center">
                                    <div class="text-center">
                                        <h1 id="auth-box-title">MeShop</h1>
                                    </div>
                                    <h5 class="pt-5 pb-5">لینک بازنشانی رمزعبور شما به ایمیلتان ارسال شد</h5>
                                </div>
                            </div>
                    </div>
                    
                    `
                    parent.html(email_message_info)

                } else if (data['status'] === 4) {
                    $('#ajax-errors').html('<p style=\'font-size: 70%!important;\'>ایمیل وارد شده در سیستم موجود نمیباشد</p>')
                    message_pop_up()

                }
            }
        });


    });

    // check user code input with user code in database for password reset
    $("#reset-password-code").submit(function (e) {

        e.preventDefault(); // avoid to execute the actual submit of the form.

        let form = $(this);
        let url = form.attr('action');
        let token = window.location.href.split('?')[1].substring(6,);

        $.ajax({
            type: "POST",
            url: url,
            data: {'token': token, 'code': $('#id_code').val()}, // serializes the form's elements.
            success: function (data) {

                // show response from the python script.
                let response_status_code = data['status'][1]
                if (response_status_code === 10) {

                    let new_url = $('#customer-form-reset-password-url').attr('data-url') + "?token=" + data['token'];
                    window.location.replace(new_url)
                } else if (response_status_code === 20) {
                    $('form div > input').val('')
                    $('#ajax-errors').html("<p style='font-size: 70%!important;'>کد وارد شده اشتباه است</p>")
                    message_pop_up()


                } else if (response_status_code === 30) {
                    $('form div > input').val('')
                    $('#ajax-errors').html('<p style=\'font-size: 70%!important;\'>مدت اعتبار درخواست شما به اتمام رسیده است. لطفا صفحه را مجددا بارگذاری کنید.</p>')
                    setTimeout(function () {
                        location.reload()
                    }, 5000);
                    refresh_code(window.location.href.split(`?`)[1].substring(6,))
                    message_pop_up()


                } else {
                    $('#ajax-errors').html('<p style=\'font-size: 70%!important;\'>درخواست شما با خطا مواجه شد لطفا صفحه را مجدد بارگذاری کنید</p>')
                    message_pop_up()
                    let new_url = $('#customer-register-login-url').attr('data-url');
                    window.location.replace(new_url)
                }
            }
        });


    });

    // post password and save
    $("#change-password-form").submit(function (e) {

        e.preventDefault(); // avoid to execute the actual submit of the form.

        let form = $(this);
        let url = form.attr('action');
        let token = window.location.href.split('?')[1].substring(6,);

        $.ajax({
            type: "POST",
            url: url,
            data: {'token': token, 'password1': $('#id_password1').val(), 'password2': $('#id_password2').val()}, // serializes the form's elements.
            success: function (data) {

                // show response from the python script.
                let response_status_code = data['status'][1]
                if (response_status_code === 10) {
                    let new_url = $('#customer-login-url').attr('data-url') + "?token=" + token + "&login_type=password";
                    window.location.replace(new_url)
                    $('#ajax-errors').html("<p style='font-size: 70%!important;'>رمز شما با موفقیت بازنشانی شد</p>")
                    message_pop_up()
                } else if (response_status_code === 20) {
                    $('form div > input').val('')
                    $('#ajax-errors').html("<p style='font-size: 70%!important;'>رمز ها باهم تطابق ندارند</p>")
                    message_pop_up()


                } else if (response_status_code === 30) {
                    $('form div > input').val('')
                    $('#ajax-errors').html('<p style=\'font-size: 70%!important;\'>لینک معتبر نمیباشد... درحال بازگشت به صفحه ی اصلی</p>')
                    message_pop_up()
                    setTimeout(function () {
                        let new_url = $('#customer-phone-form-reset-password-url').attr('data-url') + "?token=" + data['token'];
                        window.location.replace(new_url)
                    }, 5000);


                } else {
                    $('#ajax-errors').html('<p style=\'font-size: 70%!important;\'>درخواست شما با خطا مواجه شد لطفا صفحه را مجدد بارگذاری کنید</p>')
                    message_pop_up()
                    let new_url = $('#customer-register-login-url').attr('data-url');
                    window.location.replace(new_url)
                }
            }
        });


    });

    // register phone and create user in database
    $("#register-login").submit(function (e) {
        e.preventDefault(); // avoid to execute the actual submit of the form.

        let form = $(this);
        let url = form.attr('action');

        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(), // serializes the form's elements.
            success: function (data) {
                if (data['status'] === 0) {
                    let new_url = $('#customer-login-url').attr('data-url') + "?token=" + data['token'] + '&login_type=onetime_code';
                    window.location.replace(new_url)
                } else if (data['status'] === 1) {
                    let new_url = $('#customer-register-url').attr('data-url') + "?token=" + data['token'];
                    window.location.replace(new_url)
                } else if (data['status'] === 3) {
                    let new_url = $('#customer-login-url').attr('data-url') + "?token=" + data['token'] + '&login_type=password&by=email';
                    window.location.replace(new_url)

                } else if (data['status'] === 4) {
                    $('#ajax-errors').html('<p style=\'font-size: 70%!important;\'>کاربری با این ایمیل در سیستم موجود نمیباشد</p>')
                    message_pop_up()

                } else if (data['status'] === 5) {
                    $('#ajax-errors').html('<p style=\'font-size: 70%!important;\'>ورودی داده شده اشتباه است</p>')
                    message_pop_up()

                }
            }
        });


    });


    // login with password
    $("#login-password").submit(function (e) {
        e.preventDefault(); // avoid to execute the actual submit of the form.

        let form = $(this);
        let url = form.attr('action');
        let token = window.location.href.split('?')[1].substring(6,).split('&')[0]

        $.ajax({
            type: "POST",
            url: url,
            data: {'token': token, 'password': $('#id_password').val()}, // serializes the form's elements.
            success: function (data) {
                if (data['status'][1] === 20) {
                    let new_url = $('#customer-home-url').attr('data-url');
                    window.location.replace(new_url)
                } else if (data['status'][1] === 50) {
                    $('#ajax-errors').html('<p style=\'font-size: 70%!important;\'>رمز عبور اشتباه است</p>')
                    message_pop_up()

                }
            }
        });


    });

    // pop up messages
    function message_pop_up() {
        let popup = $("#myPopup");
        popup.css('visibility', 'visible')
    }

    // check user code input with user code in database
    $("#user-code").submit(function (e) {

        e.preventDefault(); // avoid to execute the actual submit of the form.

        let form = $(this);
        let url = form.attr('action');
        let token = window.location.href.split('?')[1].substring(6,).split('&')[0]
        $.ajax({
            type: "POST",
            url: url,
            data: {'token': token, 'code': $('#id_code').val()}, // serializes the form's elements.
            success: function (data) {

                // show response from the python script.
                let response_status_code = data['status'][1]
                if (response_status_code === 10) {
                    let new_url = $('#customer-home-url').attr('data-url');
                    window.location.replace(new_url)
                } else if (response_status_code === 20) {
                    $('form div > input').val('')
                    $('#ajax-errors').html("<p style='font-size: 70%!important;'>کد وارد شده اشتباه است</p>")
                    message_pop_up()

                } else if (response_status_code === 30) {
                    $('form div > input').val('')
                    $('#ajax-errors').html('<p style=\'font-size: 70%!important;\'>مدت اعتبار درخواست شما به اتمام رسیده است. لطفا صفحه را مجددا بارگذاری کنید.</p>')
                    setTimeout(function () {
                        location.reload()
                    }, 5000);
                    refresh_code(window.location.href.split(`?`)[1].substring(6,))
                    message_pop_up()

                } else {
                    $('#ajax-errors').html('<p style=\'font-size: 70%!important;\'>درخواست شما با خطا مواجه شد لطفا صفحه را مجدد بارگذاری کنید</p>')
                    message_pop_up()
                    let new_url = $('#customer-register-login-url').attr('data-url');
                    window.location.replace(new_url)
                }
            }
        });


    });

    $(document).click((event) => {
        if (!$(event.target).closest('#myPopup').length) {
            let popUp = $('#myPopup');
            if (popUp.css('visibility') !== 'hidden') {
                popUp.css('visibility', 'hidden')
            }
        }
    });

    $("#dismiss-login-errors").click(function () {
        $('#myPopup').css('visibility', 'hidden')
    })


    // convert English numbers to Persian
    function toFarsiNumber(n) {
        const farsiDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];

        return n
            .toString()
            .replace(/\d/g, x => farsiDigits[x]);
    }

    // Set the time we're counting down to
    let distance = 120000;

    let x = setInterval(function () {

        // Get today's date and time

        // Find the distance between now and the count down date
        distance -= 1000;

        // Time calculations for days, hours, minutes and seconds

        let minutes = String(Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)));
        let seconds = String(Math.floor((distance % (1000 * 60)) / 1000));
        if (minutes.length === 1) {
            minutes = "0" + minutes
        }
        if (seconds.length === 1) {
            seconds = "0" + seconds
        }
        // Output the result in an element with id="demo"
        let counter = document.getElementById("counter")
        if (counter) {
            counter.innerHTML = toFarsiNumber(minutes + ":" + seconds);
        }
        // If the count down is over, write some text
        if (distance < 0) {
            clearInterval(x);
            if (document.getElementById("counter-parent")) {
                document.getElementById("counter-parent").innerHTML = "<a class='links' href='' onclick='refresh_code(window.location.href.split(`?`)[1].substring(6,))'>ارسال مجدد کد</a>";
            }
        }
    }, 1000);

    let url = $("#categories-with-children-url").data('url')
    let detail_url = $("#category-detail-url").data('url')

    $.ajax({
        type: "GET",
        url: url,
        success: function (data) {
            let html = $("<div class='d-flex' />")
            let cleaned_data = []
            for (let object of data) {
                if (object.parent === null) {
                    cleaned_data.push(object)
                }
            }
            for (let category of cleaned_data) {

                if (category.parent === null) {
                    let class_attr = 'text-center border-right'
                    if (data.indexOf(category) === cleaned_data.length - 1) {
                        class_attr += ' border-left'
                    }
                    let parent_div = $(`<div class='${class_attr}' style='min-width: 13rem'/>`)
                    parent_div.html(`<a href="${detail_url.replace('0', category.id)}"><h6>${category.name}</h6></a>`)
                    if (category.children.length !== 0) {
                        let div = $("<div/>")
                        parent_div.append($("<hr/>"))
                        for (let child of category.children) {
                            let child_div = $("<div/>")
                            child_div.html(`<a href="${detail_url.replace('0', child.id)}"><h6>${child.name}</h6></a>`)
                            div.append(child_div)
                        }
                        parent_div.append(div)
                    }
                    html.append(parent_div)
                }
            }
            $("#category-div").html('')
            $("#category-div").append(html)
        }
    });
    window.addEventListener('click', function (e) {
        if (document.getElementById('navbar-search-form').contains(e.target)) {
            // Clicked in box
        } else {
            $("#show-results").css('display', 'none')
            $("#nav-search").val('')
        }


    });
    $("#return-to-top").click(function(event) {
        event.preventDefault();
        $("html, body").animate({ scrollTop: 0 }, "slow");
        return false;
    });

});


function show_result() {
    let url = $("#search-in-products-url").data('key')
    let product_detail = $("#product-detail-url").data('url')
    let string = $('#nav-search').val()
    if (string !== '') {
        $.ajax({
            type: "POST",
            url: url,
            data: {string: string},
            success: function (data) {
                let results = $('#show-results')
                results.html('')
                if (data.length !== 0) {
                    for (let product of data) {
                        let product_html = `
                            
                            <div class="border-solid rounded pt-1 bg-white col-12 col-md-4 text-center pb-5" style="height: available">
                                <a href="${product_detail.replace('0', product.id)}" style="text-decoration: none" class="text-dark">
                                    <img style="width: 100px" class="mr-3" src="${product.image}">
                                    <div>
                                        <h6 class="pt-1" style="line-height: 1.6rem">${product.name}</h6> 
                                        <small class="small-font mr-4">دسته: ${product.category}</small>
                                    </div>
                                </a>
                                                               
                            </div>
                 
                        `
                        results.append($(product_html))
                    }
                    results.css('display', 'flex')
                } else {
                    results.append('<div class="col-12 text-center bg-white rounded border-solid"><h5><i>نتیجه ای یافت نشد</i></h5></div>')
                    results.css('display', 'flex')
                }
            }
        });

    } else {
        $('#show-results').html('').css('display', 'none')
    }
}

function clear_cart_session() {
    localStorage.removeItem('cart_counter')
}

