function refresh_code(token) {
        let url = $('#customer-refresh-code-url').attr('data-url')
        $.ajax({
            type: "POST",
            url: url,
            data: {'token': token},
            success: function (data) {
                if (data['status'] === 20) {
                    console.log('yes')
                }
            }
        });
    }
$(document).ready(function () {

    // refresh code ajax
    if (window.location.href.includes('token') && window.location.href.includes('login_type=onetime_code')) {
        refresh_code(window.location.href.split(`?`)[1].substring(6,).split('&')[0])
    }
    else if (performance.navigation.type === performance.navigation.TYPE_RELOAD && !(window.location.href.includes('token', 'login_type=password'))) {
        refresh_code(window.location.href.split(`?`)[1].substring(6,).split('&')[0])
    }
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
                    let new_url = $('#customer-login-url').attr('data-url') + "?token=" + data['token'];
                    window.location.replace(new_url)
                } else if (data['status'] === 1) {
                    let new_url = $('#customer-register-url').attr('data-url') + "?token=" + data['token'];
                    window.location.replace(new_url)
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
        console.log(token)
        $.ajax({
            type: "POST",
            url: url,
            data: {'token': token, 'code': $('#id_code').val()}, // serializes the form's elements.
            success: function (data) {
                console.log(data)

                // show response from the python script.
                let response_status_code = data['status'][1]
                if (response_status_code === 10) {
                    let new_url = $('#customer-home-url').attr('data-url');
                    window.location.replace(new_url)
                } else if (response_status_code === 20) {
                    $('form div > input').val('')
                    $('#ajax-errors').html("<p style='font-size: 70%!important;'>کد وارد شده اشتباه است</p>")
                    message_pop_up()
                    console.log($('#myPopup'))

                } else if (response_status_code === 30) {
                    $('form div > input').val('')
                    $('#ajax-errors').html('<p style=\'font-size: 70%!important;\'>مدت اعتبار درخواست شما به اتمام رسیده است. لطفا صفحه را مجددا بارگذاری کنید.</p>')
                    setTimeout(function(){location.reload()}, 5000);
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
            document.getElementById("counter-parent").innerHTML = "<a class='links' href='' onclick='refresh_code(window.location.href.split(`?`)[1].substring(6,))'>ارسال مجدد کد</a>";
        }
    }, 1000);
});