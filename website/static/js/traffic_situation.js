// initialize the string for getting id of leaflet map
// please set it before using this js file
var leaflet_map_id = 'mymap';



function alertClick(e) {
    alert('Clicked on a polyline of ' + camera_name + '!');
    camera_name = e.target._events.click[0].ctx['camera_name']
    var popup = L.popup()
                .setLatLng(e.latlng)
                .setContent('<p>Hello world!<br />This is a nice popup of ' + camera_name + '.</p>')
                .openOn(map_for_traffic_situation);
}

function popup() {
    var popup = L.popup()
                .setLatLng([13.151226, -61.223207])
                .setContent('<p>Hello world!<br />This is a nice popup of ' + 'test' + '.</p>')
                .openOn(map_for_traffic_situation);
}

polylines = new Object()
function update_traffic_situation(detected_results) {
    for(var result_key in detected_results) {
        if (typeof(polylines[result_key]) == "undefined") {
            polylines[result_key] = L.polyline([detected_results[result_key][2],detected_results[result_key][3]], {weight: 10, color:'greed'})
            .on('click', function(e){ alertClick(e); }, {camera_name: result_key})
            .addTo(map_for_traffic_situation)
        }

        polylines[result_key].setStyle({color: detected_results[result_key][1]})
    }
}

$(window).on('load', function() {
    map_for_traffic_situation = window["Object"].values(window)[window["Object"].keys(window).indexOf(leaflet_map_id)]
    
    // initialize websocket to receive traffic situation data
    var chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/push/');

    chatSocket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var message = data['message'];
        update_traffic_situation(message)
    };

    chatSocket.onclose = function(e) {
        console.error('Pusher socket closed unexpectedly');
    };
})
