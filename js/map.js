// basic region infos
// { regionKey : { name: 'xxx', res: 12, area: 34 } }
// src:
// - residents: https://statistik.thueringen.de/datenbank/TabAnzeige.asp?tabelle=gg000102&startpage=99&vorspalte=1&felder=2&zeit=2018%7C%7Cs1
// - area: https://statistik.thueringen.de/datenbank/TabAnzeige.asp?tabelle=GG000101%7C%7C

var resultArray = {}; // contains the dataset of the actual type including the color of every region
var json = {}; // contains the received dataset
var maxArray = {}; // contains the max values for every json.type
var sumArray = {}; // contains the sum of all elements
var langKey = 'de'; // contains the used language
var currentType = ''; // selected json.type
var labelState = 'regionLabels';
var graphBlockContainerDefaultHTML = '';

function city_template_exists( regionKey ){
	var url =  './region_templates/' + regionKey + '.html';
	//console.log(url);

    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.responseType = 'html';
    request.onload = function() {
		var status = request.status;
		//console.log( status );
		if (status === 404) {
			console.log("Loading default...");

			document.getElementById( 'graphBlockContainer' ).innerHTML = graphBlockContainerDefaultHTML;
			document.getElementById( 'graph_variable' ).src='https://www.michael-böhme.de/corona/plotT1_' + regionKey + '.png';
			document.getElementById( 'graph_headline' ).innerHTML = json.values[ regionKey ]['name'];		
			document.getElementById( 'graph_variable_age_cases' ).src='https://www.michael-böhme.de/corona/plot5A_RKI_' + regionKey + '.png';
			document.getElementById( 'graph_variable_age_dec'   ).src='https://www.michael-böhme.de/corona/plot5B_RKI_' + regionKey + '.png';
		} else {
			document.getElementById( 'graphBlockContainer' ).innerHTML = request.response;
			console.log( "file exists" );
		}
    };
    request.send();
}

function js_goto( id ) {
	id = id.split('_');
	regionKey = id[1];
	document.getElementById( 'graphBlockContainer' ).style.display='block';
	/*document.getElementById( 'graph_variable' ).src='https://www.michael-böhme.de/corona/plotT1_' + regionKey + '.png';
	document.getElementById( 'graph_headline' ).innerHTML = json.values[ regionKey ]['name'];

	document.getElementById( 'graph_variable_age_cases' ).src='https://www.michael-böhme.de/corona/plot5A_RKI_' + regionKey + '.png';*/
	city_template_exists( regionKey  );
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

function hide_region_texts(	) {
	document.getElementById( 'show_value_labels' ).style.display = 'none';
	document.getElementById( 'show_name_labels' ).style.display = 'inline-block';
	for ( var region in json.values ) {
		var tspan = document.getElementById( 'tspan_' + region );
		var y = 0;
		// find all tspans, hide them and get the new y position, if more than one
		if ( tspan != null ) { 
			tspan.style = 'display:none';
		} else {
			var cnt = 0;
			for (var i = 1; i < 4; i++) {
				var tspan = document.getElementById( 'tspan' + i  + '_' + region );
				if ( tspan != null ) {
					y += tspan.getBBox().y + tspan.getBBox().height;
					tspan.style = 'display:none';
					cnt++;
				}
			}
			y = Math.round( y / cnt );
		}
		// create a new label with the value
		var node = document.createElementNS("http://www.w3.org/2000/svg", 'tspan');//createElement("tspan");
		node.setAttribute("id", 'tsc_' + region );
		node.setAttribute("style", "font-size: 24px; font-weight: bold;");
		if ( y > 0 ) node.setAttribute("y", y);
		node.innerHTML = formatValue( resultArray[ region ]['value'] );
		document.getElementById( 'text_' + region ).appendChild( node );
	}
	labelState = 'regionNumbers';
}

function show_region_texts(	) {
	document.getElementById( 'show_value_labels' ).style.display = 'inline-block';
	document.getElementById( 'show_name_labels' ).style.display = 'none';
	for ( var region in json.values ) {
		// redisplay labels
		var tspan = document.getElementById( 'tspan_' + region );
		if ( tspan != null ) { 
			tspan.style = 'display:block';
		} else {
			for (var i = 1; i < 4; i++) {
				var tspan = document.getElementById( 'tspan' + i  + '_' + region );
				if ( tspan != null ) {
					tspan.style = 'display:block';
				}
			}
		}
		//remove value label
		document.getElementById( 'tsc_' + region ).remove();
	}
	labelState = 'regionLabels';
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
		value = Math.round(value);
		result = Math.floor( value / 1000000 ) + '&thinsp;';
		if ( (Math.floor(value % 1000000) / 1000) < 10 ) {
			result += '00';
		} else if ( (Math.floor(value % 1000000) / 1000) < 10 ) {
			result += '0';
		}
		result += Math.floor((value % 1000000) / 1000) + '&thinsp;';
		if ( value % 1000 < 10 ) {
			result += '00';
		} else if ( value % 1000 < 100 ) {
			result += '0';
		}
		result += value % 1000;
	}
	else if ( value > 1000 ) {
		value = Math.round(value);
		result = Math.round( value - Math.floor( value / 1000 ) * 1000 );
		if ( result < 10 ) {
			result = '00' + result;
		} else if ( result < 100 ) {
			result = '0' + result;
		}
		result = Math.floor( value / 1000 ) + '&thinsp;' + result;
	} else {	
		var factor = 1;
		if ( value < 10 ) {
			factor = 100;
		} else if ( value < 100 ) {
			factor =  10;
		}
		result = Math.round( value * factor ) / factor;
	}
	return getPrefix( value ) + ( result < 0 ? Math.abs(result) : result ).toString().replace(".",",");
}

function showUnits( ) {
	// show units
	document.getElementById( 'cases' ).style.display = 'block';
	document.getElementById( 'cases_tspan_region' ).innerHTML = json.types[ currentType ][ 'unit' ];
	document.getElementById( 'cases_text_headline' ).style.display = 'none';
	document.getElementById( 'cases_tspan_count' ).innerHTML = '';
}

function showLegend( ) {
	// hide legend and labels
	document.getElementById( 'legend' ).style.display = 'block';
	document.getElementById( 'colorGradient' ).style.display = 'block';
	document.getElementById( 'legend_incidence' ).style.display = 'none';
}

function hideLegend( ) {
	// hide legend and labels
	document.getElementById( 'legend' ).style.display = 'none';
	document.getElementById( 'colorGradient' ).style.display = 'none';
	document.getElementById( 'legend_incidence' ).style.display = 'block';
}

function m_over_region( id ) {
	id = id.split( '_' );

	var node = document.createElementNS("http://www.w3.org/2000/svg", 'path');
	node.setAttribute( 'id', 'overlay_' + id[1] );
	node.setAttribute( 'd', document.getElementById( 'path_' + id[1] ).getAttribute('d') );
	node.setAttribute( 'class', 'borderOverlay' );
	document.getElementById( 'State_borders' ).appendChild( node );

	document.getElementById( 'cases_text_headline' ).style.display = 'block';
	document.getElementById( 'cases_tspan_region' ).innerHTML = json.values[ id[1] ]['name'];
	
	var value = formatValue( resultArray[ id[1] ]['value'] );
	if ( 'unit' in json.types[ currentType ] ) {
		if ( ( ( resultArray[ id[1] ]['value'] == '1' ) || ( resultArray[ id[1] ]['value'] == '-1' ) ) && ( 'unit1' in json.types[ currentType ] ) ) {
			value = value + ' ' + json.types[ currentType ][ 'unit1' ];
		} else {
			value = value + ' ' + json.types[ currentType ][ 'unit' ];
		}
	}
	document.getElementById( 'cases_tspan_count' ).innerHTML = value;
}

function m_out_region( id ) {
	id = id.split('_');
	document.getElementById( 'overlay_' + id[1] ).remove();
	document.getElementById( 'cases_tspan_count' ).innerHTML = '';
	showUnits( currentType );
}

function changeViewTo( id ) {
	for (var key in json.types) {
		document.getElementById( 'selector_' + key ).className = "";//.style.fontWeight = "normal";
	}
	document.getElementById( id ).className = "menu_focus";
	currentType = id.split('_')[1];
	is_7d_incidence = currentType == 'incidence';

	for (var regionKey in json.values) {
		// populate result array to be able to read out the data on mouse over
		resultArray[ regionKey ] = {};
		resultArray[ regionKey ]['value'] = json.values[ regionKey ][ currentType ];
		resultArray[ regionKey ]['color'] = valueToColor( resultArray[ regionKey ]['value'], maxArray[ currentType ], json.types[ currentType ][ 'color' ], is_7d_incidence );
		// apply color to map
		document.getElementById( 'path_'+ regionKey ).style.fill = resultArray[ regionKey ]['color'];
		document.getElementById( 'text_'+ regionKey ).setAttribute("style", "text-shadow: 2px 2px 4px " + getShadowColor( resultArray[ regionKey ]['color'] ) + ";");
		document.getElementById( 'text_'+ regionKey ).style.fill = getOverlayTextColor( resultArray[ regionKey ]['color'] );
	}
	// fix for Eisenach
	resultArray[ "EA" ] = {};
	resultArray[ "EA" ]['value'] = json.values[ "WAK" ][ currentType ];
	resultArray[ "EA" ]['color'] = valueToColor( resultArray[ "WAK" ]['value'], maxArray[ currentType ], json.types[ currentType ][ 'color' ], is_7d_incidence );
	// apply color to map
	document.getElementById( 'path_'+ "EA" ).style.fill = resultArray[ "WAK" ]['color'];
	document.getElementById( 'text_'+ "EA" ).setAttribute("style", "display: none; text-shadow: 2px 2px 4px " + getShadowColor( resultArray[ "WAK" ]['color'] ) + ";");
	document.getElementById( 'text_'+ "EA" ).style.fill = getOverlayTextColor( resultArray[ "WAK" ]['color'] );
	// show sum
	if ( 'showSum' in json.types[ currentType ] ) {
		document.getElementById( 'tspan_sum' ).innerHTML = formatValue(Math.floor(sumArray[ currentType ])) + '&thinsp;' + json.types[ currentType ][ 'unit' ] + " insgesamt";
	} else {
		document.getElementById( 'tspan_sum' ).innerHTML = "";
	}
	// set source
	document.getElementById( 'tspan_source' ).innerHTML = "Quelle: " + json.types[ currentType ][ 'source' ];
	// hide/show legend
	if ( !is_7d_incidence )
	{
		showLegend();
	} else {
		hideLegend();
	}
	// set legend upper limit
	document.getElementById( 'upperCount' ).innerHTML = formatValue( maxArray[ currentType ] );
	document.getElementById( 'mapHeadline' ).innerHTML = json.types[ currentType ][ langKey ];
	document.getElementById( 'cases_text_headline' ).innerHTML = json.types[ currentType ][ langKey ];
	showUnits();
	// init color legend
	document.getElementById('upperLimitColor').setAttribute("stop-color", valueToColor( 1, 1, json.types[ currentType ][ 'color' ], is_7d_incidence ) );
	url = window.location.href.split("#");
	window.history.pushState("", document.getElementById( 'mapHeadline' ).innerHTML, url[0] + "#" + currentType);
}

//returns first entry of json.types
function generateMenu( ) {
	del = '';
	menu = '';
	cnt = 0;
	maxItemsPerLine = 4;
	// really nasty way to sort the object by id without loosing the key
	for ( var key in json.types ) {
		json.types[key]["key"] = key;
	}
	let sorted_types = Object.values(json.types);
	sorted_types.sort( function(a, b) { return parseInt(a.id) - parseInt(b.id); });
	sorted_types.forEach( function(item){
		cnt++;
		menu = menu + del + '<span id="selector_' + item["key"] +'">' + json.types[ item["key"] ][ langKey ] + '</span>';
		if ( cnt % maxItemsPerLine ) {
			del = '<span class="menu_delimiter">| </span>';
		} else{
			del = '<br>';
		}
	});
	document.getElementById( 'selectorLinks' ).innerHTML = menu;
	for ( var key in json.types ) {
		document.getElementById( 'selector_' + key ).onclick = (
			function( e ) {
				changeViewTo( e.target.id );
				if ( labelState != 'regionLabels' ) {
					show_region_texts();
					hide_region_texts();
				} else {
					hide_region_texts();
					show_region_texts();
				}
			} 
		);
	}
	return sorted_types[0];
}

function setDataTime() {
	var months = ['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'];
	var date = new Date( json.ts * 1000 );
	var month = months[ date.getMonth() ];
	var min = date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes(); 
	var day = date.getDate() < 10 ? '0' + date.getDate() : date.getDate(); 
	document.getElementById( 'tspan_timestamp' ).innerHTML = ' Stand: ' + day + '. ' +month + ' ' + date.getFullYear() + ', ' + date.getHours() + ':' + min + ' Uhr';
}

function getMaxValues(  ) {
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

var getJSON = function(url, callback) {
    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.responseType = 'json';
    request.onload = function() {
        callback( request.status, request.response );
    };
    request.send();
};

function getData() {
	getJSON( 
		'./data/cases_thuringia.json',
		function( err, data ) {
			if ( err !== 200 ) {
				console.log( 'Something went wrong: ' + err );
			} else {
				// set as global object
				json = data;

				setDataTime( );
				getMaxValues( );
				firstentry = generateMenu( );

				// get start type
				url = window.location.href.split("#");
				startType = (url[1] in json.types) ? url[1] : firstentry["key"] ;
                
				changeViewTo( 'selector_' + startType );

				// hide case count legend
				document.getElementById( 'cases' ).style.display = 'none';

				// init mouse events on map
				var elementTypes = ['path_', 'text_'];
				for ( var region in json.values ) {
					elementTypes.forEach( elementType => {
						obj = document.getElementById( elementType + region )
						obj.onmouseover = ( function(e){ m_over_region( e.target.id ) } );
						obj.onmouseout = ( function(e){ m_out_region( e.target.id ) } );
						obj.onclick = ( function(e) { js_goto( e.target.id ) } );
					});
				}

				// show map
				graphBlockContainerDefaultHTML = document.getElementById( 'graphBlockContainer' ).innerHTML;
				city_template_exists( 'TH' );
				document.getElementById( 'needsJS' ).style.display = 'block';
				showUnits( );
				
				// initially show values
				hide_region_texts();
			}
		}
	);
}

window.onload = function () {
	getData();
}
