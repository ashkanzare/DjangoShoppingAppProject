
JalaliDate = {
    g_days_in_month: [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
    j_days_in_month: [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
};
// convert jalali date to gregorian date
JalaliDate.jalaliToGregorian = function (j_y, j_m, j_d) {
    j_y = parseInt(j_y);
    j_m = parseInt(j_m);
    j_d = parseInt(j_d);
    var jy = j_y - 979;
    var jm = j_m - 1;
    var jd = j_d - 1;

    var j_day_no = 365 * jy + parseInt(jy / 33) * 8 + parseInt((jy % 33 + 3) / 4);
    for (var i = 0; i < jm; ++i) j_day_no += JalaliDate.j_days_in_month[i];

    j_day_no += jd;

    var g_day_no = j_day_no + 79;

    var gy = 1600 + 400 * parseInt(g_day_no / 146097); /* 146097 = 365*400 + 400/4 - 400/100 + 400/400 */
    g_day_no = g_day_no % 146097;

    var leap = true;
    if (g_day_no >= 36525) /* 36525 = 365*100 + 100/4 */
    {
        g_day_no--;
        gy += 100 * parseInt(g_day_no / 36524); /* 36524 = 365*100 + 100/4 - 100/100 */
        g_day_no = g_day_no % 36524;

        if (g_day_no >= 365) g_day_no++;
        else leap = false;
    }

    gy += 4 * parseInt(g_day_no / 1461); /* 1461 = 365*4 + 4/4 */
    g_day_no %= 1461;

    if (g_day_no >= 366) {
        leap = false;

        g_day_no--;
        gy += parseInt(g_day_no / 365);
        g_day_no = g_day_no % 365;
    }

    for (var i = 0; g_day_no >= JalaliDate.g_days_in_month[i] + (i === 1 && leap); i++)
        g_day_no -= JalaliDate.g_days_in_month[i] + (i === 1 && leap);
    var gm = i + 1;
    var gd = g_day_no + 1;

    gm = gm < 10 ? "0" + gm : gm;
    gd = gd < 10 ? "0" + gd : gd;

    return [gy, gm, gd];
}


$(document).ready(function () {

    // change customer info
    $(".edit-form").submit(function (e) {
        e.preventDefault(); // avoid to execute the actual submit of the form.

        let form = $(this)
        let url = form.attr('action');

        form = form.serialize()
        if (form.includes('day') && form.includes('year') && form.includes('month')) {
            let myDate = $('#year').val() + '-' + $('#month').val() + '-' + $('#day').val(),
            dateSplitted = myDate.split("-"),
            jD = JalaliDate.jalaliToGregorian(dateSplitted[0], dateSplitted[1], dateSplitted[2]),
            jResult = jD[0] + "-" + jD[1] + "-" + jD[2];
            form = form.slice(0, form.indexOf('&year'))
            form += '&birthday=' + jResult
        }
        let customer_info = [
            'first_name',
            'last_name',
            'birthday',
            'phone',
            'email',
            'personal_id'
        ]
        form += '&'
        for (let info of customer_info) {
            if (!form.includes(info)) {
                form += info + '=&'
            }
        }

        console.log(form.slice(0, -2))
        $.ajax({
            type: "PUT",
            url: url,
            data: form.slice(0, -1), // serializes the form's elements.
            success: function (data) {
                if (data['status'] === 20) {
                    // everything is ok
                    location.reload()
                } else {
                    let error = data['errors'][Object.keys(data['errors'])[0]][0];
                    $('.edit-errors > p').html(error)
                }

            }
        });


    });

    $(".close").click(function () {
        $('.edit-errors > p').html('')
    })


});



