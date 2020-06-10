

// insert slider
$('#camera_form > div > fieldset > div.form-row.field-region_of_interest').before(
    '\
        <div class="form-row field-video-stream">\
            <div class="row" style="margin-left: 0px;">\
                <div>\
                    <label class="required" for="id_coloring_condition_slider">Coloring condition:</label>\
                </div>\
                <div>\
                    <div>\
                        <table class="condition_table">\
                            <tr>\
                                <th>Display color</th>\
                                <th colspan=3>Number of vehicles</th>\
                            </tr>\
                            <tr class="red_row">\
                                <td><label style="color:red;">Red</label></td>\
                                <td><label class="red_min" style="color:red;"></td>\
                                <td><label>~</label></td>\
                                <td><label>&infin;</label></td>\
                            </tr>\
                            <tr style="color:orange;">\
                                <td><label style="color:orange;">Orange</label></td>\
                                <td><label class="orange_min" style="color:orange;"></td>\
                                <td><label>~</label></td>\
                                <td><label class="orange_max" style="color:orange;"></td>\
                            </tr>\
                            <tr>\
                                <td><label style="display: contents;color: green;">Green</label></td>\
                                <td><label>0</label></td>\
                                <td><label>~</label></td>\
                                <td><label class="green_max" style="color: green;"></td>\
                            </tr>\
                        </table>\
                    </div>\
                    <div id="slider-range"></div>\
                    (Please drag and drop the slider to select the condition of coloring.)<br>\
                </div>\
            </div>\
        </div>\
    '
)

$( function() {
        $('#camera_form > div > fieldset > div.form-row.field-max_amount_of_green').attr('hidden','')
        $('#camera_form > div > fieldset > div.form-row.field-max_amount_of_orange').attr('hidden','')

        var default_slider_value_1 = $( "#id_max_amount_of_green" ).val()
        var default_slider_value_2 = $( "#id_max_amount_of_orange" ).val()
        
        $( "#slider-range" ).slider({
            range: true,
            min: 0,
            max: 20,
            values: [ default_slider_value_1, default_slider_value_2 ],
            slide: function( event, ui ) {
                // update values on condition table
                $( ".green_max" ).text( ui.values[ 0 ] )
                $( ".orange_min" ).text( ui.values[ 0 ] + 1 )
                $( ".orange_max" ).text( ui.values[ 1 ] )
                $( ".red_min" ).text( ui.values[ 1 ] + 1 )

                // update color of slider UI
                var left_bar_width = parseFloat(ui.values[ 0 ])/20*100
                $('.ui-slider-range-left').css('width', left_bar_width + '%')
                var right_bar_left = parseFloat(ui.values[ 1 ])/20*100
                $('.ui-slider-range-right').css('left', right_bar_left + '%')
                $('.ui-slider-range-right').css('width', 100 - right_bar_left + '%')

                // update values on the input of form
                $( "#id_max_amount_of_green" ).val( ui.values[ 0 ] )
                $( "#id_max_amount_of_orange" ).val( ui.values[ 1 ] )
            }
        });



        // create custom bar to show the color
        $('.ui-widget-header').css('background-color', 'orange')
        var left_bar_width = $( "#slider-range" ).slider( "values", 0 )/20*100

        var right_bar_left = $( "#slider-range" ).slider( "values", 1 )/20*100
        var right_bar_width = 100 - right_bar_left

        $('.ui-slider-range').before('\
            <div class="ui-slider-range-left ui-slider-range ui-corner-all" style="left: 0%; width: ' + left_bar_width + '%; background-color: green;"></div>\
        ')
        $('.ui-widget-header').after('\
            <div class="ui-slider-range-right ui-slider-range ui-corner-all" style="left: ' + right_bar_left + '%; width: ' + right_bar_width + '%; background-color: red;"></div>\
        ')

        // initialized the numbers in condition table
        $( ".green_max" ).text( $( "#slider-range" ).slider( "values", 0 ) )
        $( ".orange_min" ).text( $( "#slider-range" ).slider( "values", 0 ) + 1 )
        $( ".orange_max" ).text( $( "#slider-range" ).slider( "values", 1 ) )
        $( ".red_min" ).text( $( "#slider-range" ).slider( "values", 1 ) + 1 )
    }
);