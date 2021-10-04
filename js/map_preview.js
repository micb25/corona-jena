
var resultArray = {};
var json = null;
var maxArray = {};
var sumArray = {};
var langKey = 'de';
var svgDoc1;
var svgDoc2;
var svgDoc3;
var svgDoc4;

function setDataTime(obj) 
{
	var months = ['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'];
	var date = new Date( json.ts * 1000 );
	var month = months[ date.getMonth() ];
	var day = date.getDate() < 10 ? '0' + date.getDate() : date.getDate(); 
	obj.contentDocument.getElementById( 'tspan_timestamp' ).innerHTML = ' Stand: ' + day + '. ' +month + ' ' + date.getFullYear();
}

function showUnits(obj) {
	// show units
    var currentType = obj.getAttribute('currentType');
    var labelStr = json.types[ currentType ][ 'unit' ].replace('&thinsp;', '.');
	obj.contentDocument.getElementById( 'cases' ).style.display = 'block';
	obj.contentDocument.getElementById( 'cases_tspan_region' ).innerHTML = labelStr;
	obj.contentDocument.getElementById( 'cases_text_headline' ).style.display = 'block';
	obj.contentDocument.getElementById( 'cases_tspan_count' ).innerHTML = '';
}

function showLegend(obj) {
	// hide legend and labels
	obj.contentDocument.getElementById( 'legend' ).style.display = 'block';
	obj.contentDocument.getElementById( 'colorGradient' ).style.display = 'block';
	obj.contentDocument.getElementById( 'legend_incidence' ).style.display = 'none';
}

function hideLegend(obj) {
	// hide legend and labels
	obj.contentDocument.getElementById( 'legend' ).style.display = 'none';
	obj.contentDocument.getElementById( 'colorGradient' ).style.display = 'none';
	obj.contentDocument.getElementById( 'legend_incidence' ).style.display = 'block';
}

function hexTorgb( hexColor ) {	
	return { 
		r: parseInt( hexColor.substring(1,3), 16 ), 
		g: parseInt( hexColor.substring(3,5), 16 ),
		b: parseInt( hexColor.substring(5,7), 16 ) 
	};
}

function rgbTohex( rgbColor ) {
	var hex = function(x) {
		if ( x > 255 ) x = 255; // overflow fix...
		x = x.toString(16);
		return (x.length == 1) ? '0' + x : x;
	};
	return '#' + hex(rgbColor['r']) + hex(rgbColor['g']) + hex(rgbColor['b']);
}

// src: https://stackoverflow.com/questions/16360533/calculate-color-hex-having-2-colors-and-percent-position
function valueToColorGradient(ratio, firstColor, secondColor) {
	return {
		'r': Math.ceil( secondColor['r'] * ratio + firstColor[ 'r' ] * (1-ratio) ),
		'g': Math.ceil( secondColor['g'] * ratio + firstColor[ 'g' ] * (1-ratio) ),
		'b': Math.ceil( secondColor['b'] * ratio + firstColor[ 'b' ] * (1-ratio) )
	};
}

function valueToColor(i, max, maxColor, use_alternative_palette ) {
	if ( !use_alternative_palette ) {
		var resultColor = { r: 255, g: 255, b: 255 };
		if ( i >= 0 ) {
			var ratio = parseFloat( i ) / parseFloat( max );
			maxColorRGB = hexTorgb( maxColor );
			resultColor = valueToColorGradient(ratio, { r: 255, g: 255, b: 255 }, maxColorRGB);
		}
		return rgbTohex( resultColor );
	} else {
		// inspired by RiskLayer's 7-day-incidence color scheme
		var color_palette = [
			{ r:   0, g:   0, b:   0 },
			{ r:  91, g:  24, b: 155 },
			{ r: 178, g: 117, b: 221 },
			{ r: 172, g:  19, b:  22 },
			{ r: 235, g:  26, b:  31 },
			{ r: 241, g: 137, b:  74 },
			{ r: 254, g: 255, b: 177 },
			{ r: 255, g: 255, b: 255 }
		];
		
		if ( i >= 1000.0 ) {
			return rgbTohex( color_palette[0] );
		}
		else if ( i >= 500.0 ) {
			return rgbTohex( valueToColorGradient((i-500)/500,  color_palette[1], color_palette[0] ) );
		}
		else if ( i >= 200 ) {
			return rgbTohex( valueToColorGradient((i-200)/300,  color_palette[2], color_palette[1] ) );
		}
		else if ( i >= 100 ) {
			return rgbTohex( valueToColorGradient((i-100)/100,  color_palette[3], color_palette[2] ) );
		}
		else if ( i >= 50 ) {
			return rgbTohex( valueToColorGradient((i-50)/50,    color_palette[4], color_palette[3] ) );
		}
		else if ( i >= 35 ) {
			return rgbTohex( valueToColorGradient((i-35)/15,    color_palette[5], color_palette[4] ) );
		}
		else if ( i >= 15 ) {
			return rgbTohex( valueToColorGradient((i-15)/20,    color_palette[6], color_palette[5] ) );
		}
		return rgbTohex( valueToColorGradient(Math.max(i,0)/15, color_palette[7], color_palette[6] ) );
	}
}

function getOverlayTextColor( bgColor ) {
	var bgColorRGB = hexTorgb( bgColor );
	var resultColor = '#000000';
	hsp = Math.sqrt(
		0.299 * (bgColorRGB['r'] ** 2) +
		0.587 * (bgColorRGB['g'] ** 2) +
		0.114 * (bgColorRGB['b'] ** 2)
	);
	if ( hsp < 0.6*255 ) {
		resultColor = '#FFFFFF';
	}
	return resultColor;
}

function getShadowColor( bgColor ) {
	var bgColorRGB = hexTorgb( bgColor );
	var resultColor = '#000000';
	hsp = Math.sqrt(
		0.299 * (bgColorRGB['r'] ** 2) +
		0.587 * (bgColorRGB['g'] ** 2) +
		0.114 * (bgColorRGB['b'] ** 2)
	);
	if ( hsp > 0.6*255 ) {
		resultColor = '#808080';
	}
	return resultColor;
}

function hide_region_texts(obj) {
	for ( var region in json.values ) {
		var tspan = obj.contentDocument.getElementById( 'tspan_' + region );
		var y = 0;
		// find all tspans, hide them and get the new y position, if more than one
		if ( tspan != null ) { 
			tspan.style = 'display:none';
		} else {
			var cnt = 0;
			for (var i = 1; i < 4; i++) {
				var tspan = obj.contentDocument.getElementById( 'tspan' + i  + '_' + region );
				if ( tspan != null ) {
					y += tspan.getBBox().y + tspan.getBBox().height;
					tspan.style = 'display:none';
					cnt++;
				}
			}
			y = Math.round( y / cnt );
		}
		// create a new label with the value
		var node = obj.contentDocument.createElementNS("http://www.w3.org/2000/svg", 'tspan');//createElement("tspan");
		node.setAttribute("id", 'tsc_' + region );
		node.setAttribute("style", "font-size: 24px; font-weight: bold;");
		if ( y > 0 ) node.setAttribute("y", y);
		node.innerHTML = formatValue( resultArray[ region ]['value'] );
		obj.contentDocument.getElementById( 'text_' + region ).appendChild( node );
	}
	labelState = 'regionNumbers';
}

function getPrefix( value ) {
	prefix = '';
	if ( 'pm' in json.types[ currentType ] ) {
		if ( json.types[ currentType ][ 'pm' ] == 1 ) {
			prefix = ( value >= 0 ) ? '+' : '−';
		}
	}
	return prefix;
}

function formatValue( value ) {
	if ( ( currentType == 'incidence' ) && ( value < 0 ) )
		return "*";

	if ( value > 1000000 ) {
		result = Math.floor( value / 1000000 ) + '.';
		if ( (Math.floor(value % 1000000) / 1000) < 10 ) {
			result += '00';
		} else if ( (Math.floor(value % 1000000) / 1000) < 10 ) {
			result += '0';
		}
		result += Math.floor((value % 1000000) / 1000) + ' ';
		if ( value % 1000 < 10 ) {
			result += '00';
		} else if ( value % 1000 < 100 ) {
			result += '0';
		}
		result += value % 1000;
	}
	else if ( value > 1000 ) {
		result = Math.round( value - Math.floor( value / 1000 ) * 1000 );
		if ( result < 10 ) {
			result = '00' + result;
		} else if ( result < 100 ) {
			result = '0' + result;
		}
		result = Math.floor( value / 1000 ) + ' ' + result;
	} else {	
		var factor = 1;
		if ( value < 10 ) {
			factor = 100;
		} else if ( value < 100 ) {
			factor =  10;
		}
		result = Math.round( value * factor ) / factor;
	}
	return getPrefix( value ) + ( result < 0 ? Math.abs(result) : result ).toString().replace(".",",").replace(" ", ".");
}

function getMaxValues() 
{
	// init maxArray
	for ( var type in json.types ) {
		maxArray[ type ] = 0;
		sumArray[ type ] = 0;
	}
	// find max values and fill maxArray
	for ( var regionKey in json.values ) {
		for ( var type in json.types ) {
			sumArray[ type ] += json.values[ regionKey ][ type ];
			if ( maxArray[ type ] < json.values[ regionKey ][ type ] ) maxArray[ type ] = json.values[ regionKey ][ type ];
		}
	}
}

function m_over_region(obj, id ) {
	id = id.split( '_' );

	var node = obj.contentDocument.createElementNS("http://www.w3.org/2000/svg", 'path');
	node.setAttribute( 'id', 'overlay_' + id[1] );
	node.setAttribute( 'd', obj.contentDocument.getElementById( 'path_' + id[1] ).getAttribute('d') );
	node.setAttribute( 'class', 'borderOverlay' );
	obj.contentDocument.getElementById( 'State_borders' ).appendChild( node );

	obj.contentDocument.getElementById( 'cases_text_headline' ).style.display = 'block';
	obj.contentDocument.getElementById( 'cases_tspan_region' ).innerHTML = json.values[ id[1] ]['name'];
	
	var value = formatValue( resultArray[ id[1] ]['value'] );
	if ( 'unit' in json.types[ currentType ] ) {
		if ( ( ( resultArray[ id[1] ]['value'] == '1' ) || ( resultArray[ id[1] ]['value'] == '-1' ) ) && ( 'unit1' in json.types[ currentType ] ) ) {
			value = value + ' ' + json.types[ currentType ][ 'unit1' ];
		} else {
			value = value + ' ' + json.types[ currentType ][ 'unit' ];
		}
	}
	// obj.contentDocument.getElementById( 'cases_tspan_count' ).innerHTML = value;
}

function m_out_region(obj, id ) {
	id = id.split('_');
	obj.contentDocument.getElementById( 'overlay_' + id[1] ).remove();
	obj.contentDocument.getElementById( 'cases_tspan_count' ).innerHTML = '';
	showUnits( obj );
}

function changeViewTo(obj, id) {
	currentType = obj.getAttribute('currentType');
	is_7d_incidence = currentType == 'incidence';

	for (var regionKey in json.values) {
		// populate result array to be able to read out the data on mouse over
		resultArray[ regionKey ] = {};
		resultArray[ regionKey ]['value'] = json.values[ regionKey ][ currentType ];
		resultArray[ regionKey ]['color'] = valueToColor( resultArray[ regionKey ]['value'], maxArray[ currentType ], json.types[ currentType ][ 'color' ], is_7d_incidence );
		// apply color to map
		obj.contentDocument.getElementById( 'path_'+ regionKey ).style.fill = resultArray[ regionKey ]['color'];
		obj.contentDocument.getElementById( 'text_'+ regionKey ).setAttribute("style", "text-shadow: 2px 2px 4px " + getShadowColor( resultArray[ regionKey ]['color'] ) + ";");
		obj.contentDocument.getElementById( 'text_'+ regionKey ).style.fill = getOverlayTextColor( resultArray[ regionKey ]['color'] );
        
		// hack: apply style
		obj.contentDocument.getElementById( 'text_'+ regionKey ).style.textAlign = "center";
		obj.contentDocument.getElementById( 'text_'+ regionKey ).style.textAnchor = "middle";
	}

	// fix for Eisenach
	resultArray[ "EA" ] = {};
	resultArray[ "EA" ]['value'] = json.values[ "WAK" ][ currentType ];
	resultArray[ "EA" ]['color'] = valueToColor( resultArray[ "WAK" ]['value'], maxArray[ currentType ], json.types[ currentType ][ 'color' ], is_7d_incidence );

	obj.contentDocument.getElementById( 'path_'+ "EA" ).style.fill = resultArray[ "WAK" ]['color'];
	obj.contentDocument.getElementById( 'text_'+ "EA" ).setAttribute("style", "display: none; text-shadow: 2px 2px 4px " + getShadowColor( resultArray[ "WAK" ]['color'] ) + ";");
	obj.contentDocument.getElementById( 'text_'+ "EA" ).style.fill = getOverlayTextColor( resultArray[ "WAK" ]['color'] );
	
	// hack: apply style
	obj.contentDocument.getElementById( 'tspan_timestamp' ).style.textAlign = "center";
	obj.contentDocument.getElementById( 'tspan_timestamp' ).style.textAnchor = "middle";
	
	obj.contentDocument.getElementById( 'tspan_source' ).style.textAlign = "center";
	obj.contentDocument.getElementById( 'tspan_source' ).style.textAnchor = "middle";

	// show sum
	if ( 'showSum' in json.types[ currentType ] ) {
		obj.contentDocument.getElementById( 'tspan_sum' ).innerHTML = formatValue(Math.floor(sumArray[ currentType ])) + ' ' + json.types[ currentType ][ 'unit' ];
	} else {
		obj.contentDocument.getElementById( 'tspan_sum' ).innerHTML = "";
	}

	obj.contentDocument.getElementById( 'tspan_sum' ).style.textAlign = "center";
	obj.contentDocument.getElementById( 'tspan_sum' ).style.textAnchor = "middle"; 

	obj.contentDocument.getElementById( 'cases_tspan_region' ).innerHTML = "";

	// set source
	obj.contentDocument.getElementById( 'tspan_source' ).innerHTML = "Quelle: " + json.types[ currentType ][ 'source' ];
	// hide/show legend
	if ( !is_7d_incidence )
	{
		showLegend(obj);
	} else {
		hideLegend(obj);
	}
	// set legend upper limit
	obj.contentDocument.getElementById( 'upperCount' ).innerHTML = formatValue( maxArray[ currentType ] );
	obj.contentDocument.getElementById( 'cases_text_headline' ).innerHTML = json.types[ currentType ][ langKey ];
	if ( !is_7d_incidence )
	{
		// hack: apply style
		obj.contentDocument.getElementById( 'upperCount' ).style.textAlign = "center";
		obj.contentDocument.getElementById( 'upperCount' ).style.textAnchor = "middle";
		obj.contentDocument.getElementById( 'lowerCount' ).style.textAlign = "center";
		obj.contentDocument.getElementById( 'lowerCount' ).style.textAnchor = "middle";
		obj.contentDocument.getElementById( 'cases_tspan_region' ).style.textAlign = "center";
		obj.contentDocument.getElementById( 'cases_tspan_region' ).style.textAnchor = "middle";
		obj.contentDocument.getElementById( 'cases_text_headline' ).style.textAlign = "center";
		obj.contentDocument.getElementById( 'cases_text_headline' ).style.textAnchor = "middle";
	}
	showUnits(obj);
	// init color legend
	obj.contentDocument.getElementById('upperLimitColor').setAttribute("stop-color", valueToColor( 1, 1, json.types[ currentType ][ 'color' ], is_7d_incidence ) );
}

function js_goto( id ) {
	window.location.href = './index_map.html#' + id;
}

var getJSON = function(url, callback) {
    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.responseType = 'json';
    request.onload = function() {
        callback( request.status, request.response );
    };
    request.send();
};

function getData(obj) {
    if ( json == null )
    {
        getJSON('./data/cases_thuringia.json', function( err, data ) {
                if ( err !== 200 ) {
                    console.log( 'Something went wrong: ' + err );
                } else {
                    json = data;

				    getMaxValues();
                    getData(obj);
                }
            }
        );
    } else {

        setDataTime(obj);
        getMaxValues();
        changeViewTo(obj, 'selector_' + obj.getAttribute('currentType') );

        // init mouse events on preview map
        var elementTypes = ['path_', 'text_'];
        for ( var region in json.values ) {
            elementTypes.forEach( elementType => {
                robj = obj.contentDocument.getElementById( elementType + region )
                robj.onclick = ( function(e) { js_goto( obj.getAttribute('currentType') ) } );
            });
        }

        hide_region_texts(obj);
    }
}

function initializeMap(id) 
{
    if ( id == 1 )
    {
        svgDoc1 = document.getElementById( 'thuringiaMap1' );
        svgDoc1.setAttribute('currentType', 'incidence');
		getData(svgDoc1);
    }
    else if ( id == 2 ) 
    {
        svgDoc2 = document.getElementById( 'thuringiaMap2' );
        svgDoc2.setAttribute('currentType', 'diff');
		getData(svgDoc2);
    } 
	else if ( id == 3 ) 
    {
        svgDoc3 = document.getElementById( 'thuringiaMap3' );
        svgDoc3.setAttribute('currentType', 'diffweek');
		getData(svgDoc3);
    }
	else if ( id == 4 ) 
    {
        svgDoc4 = document.getElementById( 'thuringiaMap4' );
        svgDoc4.setAttribute('currentType', 'cases');
		getData(svgDoc4);
    }
	else if ( id == 5 ) 
    {
        svgDoc4 = document.getElementById( 'thuringiaMap5' );
        svgDoc4.setAttribute('currentType', 'deceased');
		getData(svgDoc4);
    }
}
