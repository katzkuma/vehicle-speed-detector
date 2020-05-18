// condition of doing click events, default is disabled
var createRect = false;
var moveEndPoint = false;

// for getting clicked element from HTML
var obj;

// show ROI from given data 
function show() {
    var givenROI = JSON.parse($('#id_region_of_interest').val());
    givenROI = unNormalizeResolution(givenROI);
    var points_of_poly = givenROI[0] + ' ' + givenROI[1] + ' ' + givenROI[2] + ' ' + givenROI[3];
    $('#poly').attr('points', points_of_poly);
    border($("#poly"), 'add');
}

// do mouse down event
function down(event) {
    // get clicked element from HTML
    obj = window.event ? event.srcElement : evt.target;

    if (obj.id == "ROISelector") {
        // if click on SVG element

        //remove border of ROI
        border($("#poly"), 'remove');

        // allow to create rectangular ROI on selector
        createRect = true;

        // get location of cursor from SVG element
        var startX = event.layerX;
        var startY = event.layerY;

        // create origin point of ROI
        var origin = startX + ',' + startY
        var points_of_poly = origin + ' ' + origin + ' ' + origin + ' ' + origin
        $('#poly').attr('points', points_of_poly)

    } 
    else if (obj.id == "first_poly_point" | obj.id == "second_poly_point" | obj.id == "third_poly_point" | obj.id == "fourth_poly_point") {
        // if click on dragged handle
        moveEndPoint = true
    }
}

// do mouse up event
function up(event) {
    var points_array = $("#poly").attr('points').split(' ');
    if (createRect) {
        if (points_array[0] == points_array[2]) {
            // if selected ROI is a point, not a rectangle, don't show anythings.
            $("#poly").attr('points', '0,0 0,0 0,0 0,0')
            $('#first_poly_point').attr('r', '0')
            $('#second_poly_point').attr('r', '0')
            $('#third_poly_point').attr('r', '0')
            $('#fourth_poly_point').attr('r', '0')
        }
        else {
            // if selected ROI is rectangle, show the border of it.
            border($("#poly"), 'add');
        }
    }
    
    if (createRect || moveEndPoint)
    {
        // set the selected ROI in submitting form when finish adjusting ROI
        normalized_points = normalizeResolution(points_array)
        $('#id_region_of_interest').val('{ "first_point":"' + normalized_points[0] + '", "second_point":"' + normalized_points[1] + '", "third_point":"' + normalized_points[2] + '", "fourth_point":"' + normalized_points[3] + '" }')
    }

    // disable every click events
    createRect = false;
    moveEndPoint = false;
}

// do mouse moving event
function move(event) {
    if (createRect) {
        // create rectangle

        // get cursor location from SVG element
        var endX = event.layerX;
        var endY = event.layerY;

        // show ROI on selector
        var points_array = $("#poly").attr('points').split(' ');
        var first_point = points_array[0].split(',');
        var points_of_poly = points_array[0] + ' ' + endX + ',' + first_point[1] + ' ' + endX + ',' + endY + ' ' + first_point[0] + ',' + endY;
        $('#poly').attr('points', points_of_poly)

        // allow doing mouse up event when doing moving event
        window.event.cancelBubble = true;
        window.event.returnValue = false;
    } else if (moveEndPoint) {
        // dragging handle

        // get cursor location from SVG element
        var newPoint = event.layerX + ',' + event.layerY
        
        // get current location of ROI
        var points_array = $("#poly").attr('points').split(' ');

        // set new ROI by each dragged handle
        switch (obj.id) {
            case "first_poly_point":
                var points_of_poly = newPoint +  ' ' + points_array[1] + ' ' + points_array[2] + ' ' + points_array[3];
                $('#poly').attr('points', points_of_poly)
                border($("#poly"), 'add');
                break;
            case "second_poly_point":
                var points_of_poly = points_array[0] +  ' ' + newPoint + ' ' + points_array[2] + ' ' + points_array[3];
                $('#poly').attr('points', points_of_poly)
                border($("#poly"), 'add');
                break;
            case "third_poly_point":
                var points_of_poly = points_array[0] +  ' ' + points_array[1] + ' ' + newPoint + ' ' + points_array[3];
                $('#poly').attr('points', points_of_poly)
                border($("#poly"), 'add');
                break;
            case "fourth_poly_point":
                var points_of_poly = points_array[0] +  ' ' + points_array[1] + ' ' + points_array[2] + ' ' + newPoint;
                $('#poly').attr('points', points_of_poly)
                border($("#poly"), 'add');
                break;
        }
    }

}

function border(obj, option) {
    if (option == 'add') {
        var points_array = $(obj).attr('points').split(' ');
        $('#first_poly_point').attr('cx', points_array[0].split(',')[0])
        $('#first_poly_point').attr('cy', points_array[0].split(',')[1])
        $('#first_poly_point').attr('r', '5')

        $('#second_poly_point').attr('cx', points_array[1].split(',')[0])
        $('#second_poly_point').attr('cy', points_array[1].split(',')[1])
        $('#second_poly_point').attr('r', '5')

        $('#third_poly_point').attr('cx', points_array[2].split(',')[0])
        $('#third_poly_point').attr('cy', points_array[2].split(',')[1])
        $('#third_poly_point').attr('r', '5')

        $('#fourth_poly_point').attr('cx', points_array[3].split(',')[0])
        $('#fourth_poly_point').attr('cy', points_array[3].split(',')[1])
        $('#fourth_poly_point').attr('r', '5')
    } else if (option == 'remove') {
        $('#first_poly_point').attr('r', '0')
        $('#second_poly_point').attr('r', '0')
        $('#third_poly_point').attr('r', '0')
        $('#fourth_poly_point').attr('r', '0')
    }
}

function normalizeResolution(points_array){
    // normalize the resolution between 1 and 0
    for (let index = 0; index < points_array.length; index++) {
        point = points_array[index].split(',');

        // the resolution of admin page is 760x480
        points_array[index] = point[0]/760 + ',' + point[1]/480;
    }
    return points_array
}

function unNormalizeResolution(points_JSON){
    var newArray = [];

    // unnormalize the resolution to 760 and 480
    for (let index = 0; index < Object.keys(points_JSON).length; index++) {
        point = Object.values(points_JSON)[index].split(',');

        // the resolution of admin page is 760x480
        newArray.push(point[0]*760 + ',' + point[1]*480);
    }
    return newArray
}