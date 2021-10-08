let global_map;
let map_backup;

function show_map() {

    mapboxgl.setRTLTextPlugin('https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.2.0/mapbox-gl-rtl-text.js');
    setTimeout(function () {


        mapboxgl.accessToken = 'pk.eyJ1IjoiYXNoa2FuemFyZTc3IiwiYSI6ImNrdWZ1b2FoNTF4dWQyb21vczgxbGZsOHEifQ.9LQi28kHk1AiPl9NEj1GLA';
        let map = new mapboxgl.Map({
            container: 'map', // container id
            style: {
                'version': 8,
                'sources': {
                    'raster-tiles': {
                        'type': 'raster',
                        'tiles': [
                            'https://map.ir/shiveh/xyz/1.0.0/Shiveh:Shiveh@EPSG:3857@png/{z}/{x}/{y}.png?x-api-key=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImRiNDRhMTlhYzg5MDY0OTFjOGQxNWEwYWMzOWNlZmY3MTkwYTcwZjhiNDkzODhjZjBlNmQwZTY3ODZlMzRjZTkwYzg1NjNhY2VkNmRmMGE5In0.eyJhdWQiOiIxNTcxMCIsImp0aSI6ImRiNDRhMTlhYzg5MDY0OTFjOGQxNWEwYWMzOWNlZmY3MTkwYTcwZjhiNDkzODhjZjBlNmQwZTY3ODZlMzRjZTkwYzg1NjNhY2VkNmRmMGE5IiwiaWF0IjoxNjMzNTUxMDMzLCJuYmYiOjE2MzM1NTEwMzMsImV4cCI6MTYzNjA1NjYzMywic3ViIjoiIiwic2NvcGVzIjpbImJhc2ljIl19.b5i1-HZ0WFGASeWs20XtVBsQV5QeG-zf_fD53k0V_IMRBK_X4oCSIZ_F-6aR1AZNWWX21K4gQ-yx0dyYjWU7YpOHP-u7MMBiV_LnQ4uNbgyS3rrsIwjL-n-FBZUBLf27pJhZ2gXMNP5ne4lTCsiblams6zwajlpQc0ywoeRCmjvWMbjZojA0iVG0FfiOOste-i_qjoGrLYZlI5jYzMiFk53es1fBUtQsRYl9GDyGLkO09drUc6ZcMGsBYlnak_eUKSDWNJQJFRJ4lDoZtIbciziA7BbsCJVw_FSdALLipjI64g6CnmIkztmXlf8HqseQySs5bPPaZE_IuiGJ_dAEAw'
                        ],
                        'tileSize': 256,
                        'attribution':
                            'Map tiles by <a target="_top" rel="noopener" href="http://stamen.com">Stamen Design</a>, under <a target="_top" rel="noopener" href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a target="_top" rel="noopener" href="http://openstreetmap.org">OpenStreetMap</a>, under <a target="_top" rel="noopener" href="http://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>'
                    }
                },
                'layers': [
                    {
                        'id': 'simple-tiles',
                        'type': 'raster',
                        'source': 'raster-tiles',
                        'minzoom': 0,
                        'maxzoom': 22
                    }
                ]
            },
            center: [51.33776109571264, 35.70000461459449], // starting position
            zoom: 14.5 // starting zoom
        });
        map.on('load', function () {
            map.resize();
        });
        map.on('style.load', function () {
            map.on('click', function (e) {
                let coordinates = e.lngLat;
                new mapboxgl.Popup()
                    .setLngLat(coordinates)
                    .setHTML('you clicked here: <br/>' + coordinates)
                    .addTo(map);
            });
        });
        map.addControl(
            new mapboxgl.GeolocateControl({
                positionOptions: {
                    enableHighAccuracy: true
                },
// When active the map will receive updates to the device's location as it changes.
                trackUserLocation: true,
// Draw an arrow next to the location dot to indicate which direction the device is heading.
                showUserHeading: true
            })
        );
        global_map = map
    }, 100);
}

// get all cities and provinces
let places_select;
$(document).ready(function () {
    let api_url = $('#city-province-url').data('key')
    $.ajax({
        type: "GET",
        url: api_url,
        success: function (data) {
            console.log(data)
            places_select = `<select class="form-control" id="provinces">`
            for (let i in data) {
                let option = `<option value="${i}">${i}</option>`

                places_select += option
            }
            places_select += '</select>'
        }

    })


})

// get csrf token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// address details modal
function address_details(address_list, address_str) {
    let modal_title = $('.modal-title')
    let modal_body = $('#address-body')
    let api_url = $('#city-province-url').data('key')
    let select = places_select

    modal_title.html('جزییات آدرس')
    let address_form = `
    <form class="text-right p-5" id="address-form" method="post" style="border-top: 1px solid black" onsubmit="return validateAddressForm()">
            <input type="hidden" name="csrfmiddlewaretoken" value="${getCookie('csrftoken')}">
            <div class="d-flex justify-content-center mb-2">
                <div id="address-form-errors" class="text-center d-none error-div pr-5 pl-5"></div>
            </div>
            <div class="form-row mb-4">
            
                <div class="col">
                    <!-- Province -->
                    <label for="province">استان<sup>*</sup></label>                 
                    ${select}
                </div>
                <div id="cities-div" class="col">
                    <!-- City -->
                    <label for="city">شهر<sup>*</sup></label>
                    
                </div>
            </div>

            <!-- address -->
            <label for="address">نشانی پستی<sup>*</sup></label>
            <input type="text" id="address" name="address" class="form-control mb-4" value="${address_str}">


            <div class="form-row mb-4">
                <div class="col">
                    <!-- building number -->
                    <label for="building_number">پلاک<sup>*</sup></label>
                    <input type="text" id="building_number" name="building_number" maxlength="4" class="form-control">
                </div>

                <div class="col">
                    <!-- building unit -->
                    <label for="building_unit">واحد<sup>*</sup></label>
                    <input type="text" id="building_unit" name="building_unit" class="form-control" maxlength="4">
                </div>

                <div class="col-6">
                    <!-- postal code -->
                    <label for="postal_code">کد پستی<sup>*</sup></label>
                    <input type="text" id="postal_code" name="postal_code" maxlength="10" class="form-control">
                    <small>کدپستی باید ۱۰ رقم و بدون خط تیره باشد</small>
                </div>
            </div>

            <hr>
            <div class="form-check text-right pb-5">
                <input type="checkbox" id="receiver" name="receiver" class="form-check-input">
                <label class="form-check-label mr-5"  for="receiver">گیرنده سفارش خودم هستم</label>
            </div>
            <div>
                <div class="form-row mb-4">
                    <div class="col">
                        <!-- receiver first name -->
                        <label for="receiver_first_name">نام گیرنده<sup>*</sup></label>
                        <input type="text" id="receiver_first_name" name="receiver_first_name" class="form-control">
                    </div>

                    <div class="col">
                        <!-- receiver last name -->
                        <label for="receiver_last_name">نام خانوادگی گیرنده<sup>*</sup></label>
                        <input type="text" id="receiver_last_name" name="receiver_last_name" class="form-control">
                    </div>

                    <div class="col-12">
                        <!-- receiver phone -->
                        <label for="receiver_phone">شماره موبایل<sup>*</sup></label>
                        <input type="text" id="receiver_phone" name="receiver_phone" class="form-control">
                        <small>مثل: ۰۹۱۲۳۴۵۶۷۸۹</small>
                    </div>
                </div>
            </div>

            <div class="d-flex justify-content-around pt-3 mt-3" style="border-top: 1px solid black">
                    <button class="small-font mt-1 link-buttons text-primary" onclick="refresh_map()">اصلاح موقعیت روی نقشه</button>
                    <button style="min-width: 10rem!important;" class="btn btn-danger" type="submit">
                       تایید و ثبت آدرس
                    </button>
            </div>
        </form>
    
    `
    $('#MAP').css('display', 'none')
    modal_body.append($(address_form))
    let select_parent = $('#provinces')

    $('#address-form input').click(function () {
        console.log($(this))
        $(this).css('box-shadow', 'none').css('outline', 'none')
    })

    let options = select_parent.children()
    for (let option of options) {
        if ($(option).html().normalize() === address_list[0].normalize()) {
            $(option).prop("selected", true)
        }
    }
    let province = select_parent.val()


    $.ajax({
        type: "POST",
        url: api_url,
        data: {name: province.normalize()},
        success: function (data) {
            console.log(data)
            let cities_select = `<select class="form-control" id="cities">`
            for (let i of data.cities) {
                let option = `<option value="${i}">${i}</option>`

                cities_select += option
            }
            cities_select += '</select>'
            $('#cities-div').append(cities_select)
        }

    })

    select_parent.change(function () {
        let new_province = select_parent.val()
        $.ajax({
            type: "POST",
            url: api_url,
            data: {name: new_province.normalize()},
            success: function (data) {
                console.log(data)
                let cities_select = `<select class="form-control" id="cities">`
                for (let i of data.cities) {
                    let option = `<option value="${i}">${i}</option>`

                    cities_select += option
                }
                cities_select += '</select>'
                $('#cities').remove()
                $('#cities-div').append(cities_select)
            }

        })
    });

    $('#receiver').click(function () {
        let checked = $('#receiver').is(":checked");

        if (checked) {
            let receiver_first_name = $('#receiver_first_name')
            let receiver_last_name = $('#receiver_last_name')

            let first_name = $('#first_name').data('key')
            let last_name = $('#last_name').data('key')

            if (first_name !== 'None') {
                receiver_first_name.val(first_name).prop('disabled', true)
            }
            if (last_name !== 'None') {
                receiver_last_name.val(last_name).prop('disabled', true)
            }
            $('#receiver_phone').val(`0${$('#phone').data('key')}`).prop('disabled', true);
        } else {
            $('#receiver_first_name').val('').prop('disabled', false);
            $('#receiver_last_name').val('').prop('disabled', false);
            $('#receiver_phone').val('').prop('disabled', false);
        }
    });

}


// get coordinate from map and convert to address
function get_coordinate() {
    let location = global_map.getCenter()
    let lat = location.lat
    let lng = location.lng
    console.log(location)
    let url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${lng},${lat}.json?&access_token=pk.eyJ1IjoianNjYXN0cm8iLCJhIjoiY2s2YzB6Z25kMDVhejNrbXNpcmtjNGtpbiJ9.28ynPf1Y5Q8EyB_moOHylw`
    let translate_url = $('#city-province-translate-url').data('key')

    let fa_province;
    let fa_city;
    let fa_section;
    let address_list = [];
    $.ajax({
        type: "GET",
        url: url,
        success: function (data) {

            let location_address = data.features[0].place_name.split(',')
            let province = location_address.slice(-2, -1)[0].trim()
            let city = location_address.slice(-3, -2)
            let section = location_address.slice(-4, -3)
            if (city.length !== 0) {
                city = city[0].trim()
            } else {
                city = ''
            }
            if (section.length !== 0) {
                section = section[0].trim()
            } else {
                section = ''
            }
            fa_section = section

            const province_city = [
                {name: province},
                {name: city, is_city: true}]

            for (let place_data of province_city) {
                $.ajax({
                    type: "POST",
                    url: translate_url,
                    data: place_data,
                    success: function (data) {
                        let fa_place;
                        if ('error' in data) {
                            fa_place = null
                        } else {
                            fa_place = data.name
                        }

                        if (data.is_city !== false) {
                            fa_city = fa_place
                            address_list.push(fa_city)
                            address_list.push(fa_section)
                            setTimeout(function () {
                                address_details(address_list, address_list.slice(1).join('-'))
                            }, 500)
                        } else {
                            fa_province = fa_place
                            address_list.push(fa_province)
                        }

                    }
                })

            }


        }

    })

}

// refresh map
function refresh_map() {
    $('#address-form').remove()
    $('#MAP').css('display', 'block')

}

// get element and set it's display to none
function display_none(elem_id) {
    $(elem_id).css('display', 'none')
}

// validate address form
function validateAddressForm() {
    var container, inputs, index;

    container = document.getElementById('address-form');

    inputs = container.getElementsByTagName('input');
    let check = ''
    $('#address-form input').css('box-shadow', 'none').css('outline', 'none')
    for (index = 0; index < inputs.length; ++index) {

        if (inputs[index].value === '') {
            console.log(inputs[index].id)
            check = 'empty'
            $('#' + inputs[index].id).css('box-shadow', '0 0 3px 0 red').css('outline', 'red 1px solid')

        }
    }
    if (check === 'empty') {
        let error_div = $('#address-form-errors').attr('class', 'text-center pb-2 error-div pr-5 pl-5').css('display', 'block')
        let error = `<i class="fa fa-exclamation-circle text-danger" aria-hidden="true"></i>
                    <span  class="text-danger small-font">لطفا فیلد های زیر را پر کنید</span>
                    <div class="float-left mr-5">
                        <button type="button" class="close text-danger" onclick="display_none('#address-form-errors')">&times;</button>
                    </div>
                    `
        error_div.html(error)
        return false;
    }

    // check postal code and building number
    let postal_code = $("#postal_code")
    let building_number = $("#building_number")

    let inputs_obj = {
        'کد پستی ': postal_code,
        'پلاک ': building_number
    }

    const IsNumeric = (num) => /^-{0,1}\d*\.{0,1}\d+$/.test(num);
    for (let input in inputs_obj) {
        let elem = inputs_obj[input]
        if (!IsNumeric(elem.val())) {
            let error_div = $('#address-form-errors').attr('class', 'text-center pb-2 error-div pr-5 pl-5').css('display', 'block')
            let error = `<i class="fa fa-exclamation-circle text-danger" aria-hidden="true"></i>
                        <span  class="text-danger small-font"> ${input}باید فقط شامل ارقام باشد </span>
                        <div class="float-left mr-5">
                            <button type="button" class="close text-danger" onclick="display_none('#address-form-errors')">&times;</button>
                        </div>
                        `
            elem.css('box-shadow', '0 0 3px 0 red').css('outline', 'red 1px solid')
            error_div.html(error)
            return false;
        }
    }
    // check postal code length
    if (postal_code.length !== 10) {
            let error_div = $('#address-form-errors').attr('class', 'text-center pb-2 error-div pr-5 pl-5').css('display', 'block')
            let error = `<i class="fa fa-exclamation-circle text-danger" aria-hidden="true"></i>
                        <span  class="text-danger small-font"> کد پستی باید شامل ۱۰ رقم باشد </span>
                        <div class="float-left mr-5">
                            <button type="button" class="close text-danger" onclick="display_none('#address-form-errors')">&times;</button>
                        </div>
                        `
            postal_code.css('box-shadow', '0 0 3px 0 red').css('outline', 'red 1px solid')
            error_div.html(error)
            return false;
    }
    // check phone number
    var regex = new RegExp('^09\\d{9}$');
    let phone = $('#receiver_phone')
    var result = regex.test(phone.val());
    if (!result) {
            let error_div = $('#address-form-errors').attr('class', 'text-center pb-2 error-div pr-5 pl-5').css('display', 'block')
            let error = `<i class="fa fa-exclamation-circle text-danger" aria-hidden="true"></i>
                        <span  class="text-danger small-font"> شماره تلفن وارد شده نامعتبر است </span>
                        <div class="float-left mr-5">
                            <button type="button" class="close text-danger" onclick="display_none('#address-form-errors')">&times;</button>
                        </div>
                        `
            phone.css('box-shadow', '0 0 3px 0 red').css('outline', 'red 1px solid')
            error_div.html(error)
            return false;
        }

}

