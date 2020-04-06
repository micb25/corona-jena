// basic region infos
// { region_key : { name: 'xxx', res: 12, area: 34 } }
// src:
// - residents: https://statistik.thueringen.de/datenbank/TabAnzeige.asp?tabelle=gg000102&startpage=99&vorspalte=1&felder=2&zeit=2018%7C%7Cs1
// - area: https://statistik.thueringen.de/datenbank/TabAnzeige.asp?tabelle=GG000101%7C%7C

var resultArray = {}; // contains the dataset of the actual type including the color of every region
var json = {}; // containes the received dataset
var maxArray = {}; // contains the max values for every json.type
var langKey = 'de'; // contains the used language
var actualType = ''; // selected json.type
var labelState = 'regionLabels';
		
function js_goto( id ) {
	id = id.split('_');

	document.getElementById( 'graphBlockContainer' ).style.display='block';
	document.getElementById( 'graph_variable' ).src='https://www.michael-böhme.de/corona/plotT1_' + id[1] + '.png';
	document.getElementById( 'graph_headline' ).innerHTML = json.values[ id[1] ]['name'];
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
function valueToColor(i, max, maxColor ) {
	outputType = typeof outputType !== 'undefined' ? outputType : 'hex';
	whiteRGB = { r: 255, g: 255, b: 255 };
	var resultColor = whiteRGB;
	if ( i > 0 ) {
		var ratio = parseFloat( i ) / parseFloat( max );
		maxColorRGB = hexTorgb( maxColor );
		resultColor['r'] = Math.ceil( maxColorRGB['r'] * ratio + whiteRGB[ 'r' ] * (1-ratio) );
		resultColor['g'] = Math.ceil( maxColorRGB['g'] * ratio + whiteRGB[ 'g' ] * (1-ratio) );
		resultColor['b'] = Math.ceil( maxColorRGB['b'] * ratio + whiteRGB[ 'b' ] * (1-ratio) );

	}
	return rgbTohex( resultColor );
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

function hide_region_texts(	) {
	document.getElementById( 'show_value_labels' ).style.display = 'none';
	document.getElementById( 'show_name_labels' ).style.display = 'inline';
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
		if ( y > 0 ) node.setAttribute("y", y);
		node.innerHTML = formatValue( resultArray[ region ]['value'] );
		document.getElementById( 'text_' + region ).appendChild( node );
	}
	labelState = 'regionNumbers';
}

function show_region_texts(	) {
	document.getElementById( 'show_value_labels' ).style.display = 'inline';
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
	if ( 'pm' in json.types[ actualType ] ) {
		if ( json.types[ actualType ][ 'pm' ] == 1 ) {
			prefix = ( value >= 0 ) ? '+ ' : '- ';
		}
	}
	return prefix;
}

function formatValue( value ) {
	if ( value > 1000 ) {
		result = Math.floor( value / 1000 ) + ' ' + Math.round( value - Math.floor( value / 1000 ) * 1000 );
	} else {	
		var factor = 1;
		if ( value < 10 ) {
			factor = 100;
		} else if ( value < 100 ) {
			factor =  10;
		}
		result = Math.round( value * factor ) / factor;
	}
	return getPrefix( value ) + result.toString().replace(".",",");
}

function showUnits( ) {
	// show units
	document.getElementById( 'cases' ).style.display = 'block';
	document.getElementById( 'cases_tspan_region' ).innerHTML = json.types[ actualType ][ 'unit' ];
	document.getElementById( 'cases_text_headline' ).style.display = 'none';
	document.getElementById( 'cases_tspan_count' ).innerHTML = '';
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
	if ( 'unit' in json.types[ actualType ] ) {
		value = value + ' ' + json.types[ actualType ][ 'unit' ];
	}
	document.getElementById( 'cases_tspan_count' ).innerHTML = value;
}

function m_out_region( id ) {
	id = id.split('_');
	document.getElementById( 'overlay_' + id[1] ).remove();
	document.getElementById( 'cases_tspan_count' ).innerHTML = '';
	showUnits( actualType );
}

function changeViewTo( id ) {
	for (var key in json.types) {
		document.getElementById( 'selector_' + key ).style.fontWeight = "normal";
	}
	document.getElementById( id ).style.fontWeight = "bold";
	actualType = id.split('_')[1];

	for (var regionKey in json.values) {
		// populate result array to be able to read out the data on mouse over
		resultArray[ regionKey ] = {};
		resultArray[ regionKey ]['value'] = json.values[ regionKey ][ actualType ];
		resultArray[ regionKey ]['color'] = valueToColor( resultArray[ regionKey ]['value'], maxArray[ actualType ], json.types[ actualType ][ 'color' ] );
		// apply color to map
		document.getElementById( 'path_'+ regionKey ).style.fill = resultArray[ regionKey ]['color'];
		document.getElementById( 'text_'+ regionKey ).style.fill = getOverlayTextColor( resultArray[ regionKey ]['color'] );
		
	}
	// set legend upper limit
	value = formatValue( maxArray[ actualType ] );
	document.getElementById( 'upperCount' ).innerHTML = value;
	document.getElementById( 'mapHeadline' ).innerHTML = json.types[ actualType ][ langKey ] + ' in Thüringen';
	document.getElementById( 'cases_text_headline' ).innerHTML = json.types[ actualType ][ langKey ];
	showUnits();
	// init color legend
	document.getElementById('upperLimitColor').setAttribute("stop-color", valueToColor( 1, 1, json.types[ actualType ][ 'color' ] ) );
}

function generateMenu( ) {
	del = '';
	menu = '';
	cnt = 0;
	maxItemsPerLine = 5;
	for ( var key in json.types ) {
		cnt++;
		menu = menu + del + '<span id="selector_' + key +'">' + json.types[ key ][ langKey ] + '</span>';
		if ( cnt % maxItemsPerLine ) {
			del = '&nbsp;|&nbsp;';
		} else{
			del = '<br>';
		}
	}
	
	document.getElementById( 'selectorLinks' ).innerHTML = menu;
	for ( var key in json.types ) {
		document.getElementById( 'selector_' + key ).onclick = (function(e) {
				changeViewTo( e.target.id );
				if ( labelState != 'regionLabels' ) show_region_texts();
			} );
	}
	
}

function setDataTime() {
	var months = ['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'];
	var date = new Date( json.ts * 1000 );
	var month = months[ date.getMonth() ];
	var min = date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes(); 
	var day = date.getDate() < 10 ? '0' + date.getDate() : date.getDate(); 
	document.getElementById( 'tspan_timestamp' ).innerHTML = 'Stand: ' + day + '. ' +month + ' ' + date.getFullYear() + ', ' + date.getHours() + ':' + min + ' Uhr';
}

function getMaxValues(  ) {
	// init maxArray
	for ( var type in json.types ) {
		maxArray[ type ] = 0;
	}
	// find max values and fill maxArray
	for ( var regionKey in json.values ) {
		for ( var type in json.types ) {
			if ( maxArray[ type ] < json.values[ regionKey ][ type ] ) maxArray[ type ] = json.values[ regionKey ][ type ];
		}
	}
}

var getJSON = function(url, callback) {
    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.responseType = 'json';
    request.onload = function() {
      var status = request.status;
      if (status === 200) {
        callback(null, request.response);
      } else {
        callback(status, request.response);
      }
    };
    request.send();
};

function getData() {
	getJSON( 
		'./data/cases_thuringia.json',
		function( err, data ) {
			if ( err !== null ) {
				console.log( 'Something went wrong: ' + err );
			} else {
				// set as global object
				json = data;
				setDataTime( );
				
				getMaxValues( );
				generateMenu( );

				// get start type
				url = window.location.href.split("#");
				startType = (url[1] in json.types) ? url[1] : Object.keys( json.types )[0] ;
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
				document.getElementById( 'thuringiaMap' ).style.display = 'block';
				showUnits( );
			}
		}
	);
}

window.onload = function () {
	getData();
}
