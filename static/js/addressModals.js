let global_map;

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


function get_coordinate() {
    let location = global_map.getCenter()
    let lat = location.lat
    let lng = location.lng
    console.log(location)
    let url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${lng},${lat}.json?&access_token=pk.eyJ1IjoianNjYXN0cm8iLCJhIjoiY2s2YzB6Z25kMDVhejNrbXNpcmtjNGtpbiJ9.28ynPf1Y5Q8EyB_moOHylw`
    let translate_url = $('#city-province-translate-url').data('key')
    $.ajax({
        type: "GET",
        url: url,
        success: function (data) {
            let location_address = data.features[0].place_name.split(',')
            console.log(location_address)
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
            const province_city = [
                {name: province},
                {name: city, is_city: true}]

            let fa_province;
            let fa_city;
            for (let place_data of province_city) {
                $.ajax({
                    type: "POST",
                    url: translate_url,
                    data: place_data,
                    success: function (data) {

                    }
                })
            }
        }
    })
}
