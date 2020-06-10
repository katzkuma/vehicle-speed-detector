var polyline, mymap, camera
  
function dragStartHandler (e) {
    var latlngs = polyline.getLatLngs(),
        latlng = this.getLatLng();
    for (var i = 0; i < latlngs.length; i++) {
        if (latlng.equals(latlngs[i])) {
            this.polylineLatlng = i;
        }
    }
}
  
function dragHandler (e) {
    var latlngs = polyline.getLatLngs(),
        latlng = this.getLatLng();
    latlngs.splice(this.polylineLatlng, 1, latlng);
    polyline.setLatLngs(latlngs);
}

function dragEndHandler (e) {
    delete this.polylineLatlng;
    var latlngs = polyline.getLatLngs()
    $('#id_first_lat_recognition_section').val(parseFloat(latlngs[0]['lat']).toFixed(6))
    $('#id_first_lng_recognition_section').val(parseFloat(latlngs[0]['lng']).toFixed(6))
    $('#id_second_lat_recognition_section').val(parseFloat(latlngs[1]['lat']).toFixed(6))
    $('#id_second_lng_recognition_section').val(parseFloat(latlngs[1]['lng']).toFixed(6))
}

function addPolyline (option, latlngs) {
    if (option == 'given') {
        var a = new L.LatLng(latlngs[0], latlngs[1]),
            b = new L.LatLng(latlngs[2], latlngs[3]);
        
        var marker_a = new L.Marker(a, {draggable: true}).addTo(mymap),
            marker_b = new L.Marker(b, {draggable: true}).addTo(mymap);

    } else if (option == 'new') {
        $('#createPolyline_id').prop('disabled', true);
        var map_center = mymap.getCenter();
        var a = new L.LatLng(map_center['lat'], map_center['lng']),
            b = new L.LatLng(map_center['lat'], map_center['lng']);

        var marker_a = new L.Marker(a, {draggable: true}).addTo(mymap),
            marker_b = new L.Marker(b, {draggable: true}).addTo(mymap);
    }

    polyline = new L.Polyline([a, b]).addTo(mymap);

    marker_a
    .on('dragstart', dragStartHandler)
    .on('drag', dragHandler)
    .on('dragend', dragEndHandler);

    marker_b
    .on('dragstart', dragStartHandler)
    .on('drag', dragHandler)
    .on('dragend', dragEndHandler);

    return polyline
}

// create a web map by using API of Leaflet.js
function create_map() {
    // hide build-in detected section input for showing section selector
    $('#camera_form > div > fieldset > div.form-row.field-first_lat_recognition_section').attr('hidden','')
    $('#camera_form > div > fieldset > div.form-row.field-first_lng_recognition_section').attr('hidden','')
    $('#camera_form > div > fieldset > div.form-row.field-second_lat_recognition_section').attr('hidden','')
    $('#camera_form > div > fieldset > div.form-row.field-second_lng_recognition_section').attr('hidden','')

    // insert map container
    $('#camera_form > div > fieldset > div.form-row.field-first_lat_recognition_section').before(
        '\
            <div class="form-row field-video-stream">\
                <div class="row" style="margin-left: 0px;">\
                    <div>\
                        <label class="required" for="id_section_selector">Detected section:</label>\
                    </div>\
                    <div>\
                        (Please drag and drop the marker to select the road section which camera detect.)\
                        <div id="mapid"></div>\
                    </div>\
                </div>\
            </div>\
        '
    )

    // use API of Leaflet.js
    mymap = L.map('mapid').setView([13.154307, -61.223435], 18);
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1Ijoia2F0emt1bWEiLCJhIjoiY2s5eXFmdTdoMHk0NDNlcGJ2b2lidjM3ayJ9.cc3ys8VvRiEOgAemK5cS4Q'
    }).addTo(mymap);
}

function add_marker_camera() {
    var camera_latlng = new L.LatLng($('#id_camera_latitude').val(), $('#id_camera_longitude').val())

    var camera_icon = L.icon({
        iconUrl: '/static/images/camera.png',
        shadowUrl: 'leaf-shadow.png',
    
        iconSize:     [48, 64], // size of the icon
        shadowSize:   [50, 64], // size of the shadow
        iconAnchor:   [0, 64], // point of the icon which will correspond to marker's location
        shadowAnchor: [4, 62],  // the same for the shadow
        popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
    });

    camera = new L.Marker(camera_latlng, {draggable: false, icon: camera_icon})
            .on('mouseup', function(e){ alert('Please change the location of camera from the field above.');  })
            .addTo(mymap)
}

// create the given section from database on the map if there is it
function show_given_section() {
    // initialize the array for getting lats and lngs
    var latlngs = Array()

    // initialize the variable for checking if there is section
    var is_latlng_given = true

    latlngs.push(JSON.parse($('#id_first_lat_recognition_section').val()))
    latlngs.push(JSON.parse($('#id_first_lng_recognition_section').val()))
    latlngs.push(JSON.parse($('#id_second_lat_recognition_section').val()))
    latlngs.push(JSON.parse($('#id_second_lng_recognition_section').val()))

    latlngs.every(element => {
        if (parseInt(element) == 0){
            is_latlng_given = false

            $('#mapid').before('<button id="createPolyline_id" onclick="addPolyline(\'new\'); return false;">Create a section</button>')
            return false
        }
    });

    if (is_latlng_given) {
        polyline = addPolyline ('given', latlngs)
        mymap.panTo(polyline.getCenter());
    }
}

function show_given_camera() {
    add_marker_camera()
    $("#id_camera_latitude").change(function(){   
        camera.setLatLng(new L.LatLng($('#id_camera_latitude').val(), $('#id_camera_longitude').val()))
    });
    
    $("#id_camera_longitude").change(function(){
        camera.setLatLng(new L.LatLng($('#id_camera_latitude').val(), $('#id_camera_longitude').val()))
    });
}

create_map();
show_given_section();
show_given_camera();
