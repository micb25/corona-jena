var regions = {
	ABG: "Altenburger Land",
	EIC: "Eichsfeld",
	EA:  "Eisenach",
	EF:  "Erfurt",
	G:   "Gera",
	GTH: "Gotha",
	GRZ: "Greiz",
	HBN: "Hildburghausen",
	IK:  "Ilm-Kreis",
	J:   "Jena",
	KYF: "Kyffhäuserkreis",
	NDH: "Nordhausen",
	SHK: "Saale-Holzland-Kreis",
	SOK: "Saale-Orla-Kreis",
	SLF: "Saalfeld-Rudolstadt",
	SM:  "Schmalkalden-Meiningen",
	SOM: "Sömmerda",
	SON: "Sonneberg",
	SHL: "Suhl",
	UH:  "Unstrut-Hainich-Kreis",
	WAK: "Wartburgkreis",
	WE:  "Weimar",
	AP:  "Weimarer Land"};

// map types and colors
// { var_key : { de: 'xxx', en: 'xxx', color: '#000000' } }
var types = {
	cases : {
		de: 'Fallzahlen',
		color: '#0000D3' },
	diff : {
		de: 'Entwicklung der Fallzahlen',
		color: '#A000FF' },
	hosp : {
		de: 'Stationäre Fälle',
		color: '#FFAD00' },
	serv : {
		de: 'Schwere Fallverläufe',
		color: '#D30000' },
	death : {
		de: 'Verstorbene', 
		color: '#333333' }
};

var resultArray = {};
var fullResultArray = {};
var maxArray = {};
var langKey = 'de';
		
function js_goto( id ) {
	id = id.split('_');

	document.getElementById( 'graphBlockContainer' ).style.display='block';
	document.getElementById( 'graph_variable' ).src='https://www.michael-böhme.de/corona/plotT1_' + id[1] + '.png';
	document.getElementById( 'graph_headline' ).innerHTML=regions[ id[1] ];
}

// src: https://stackoverflow.com/questions/16360533/calculate-color-hex-having-2-colors-and-percent-position
function value_to_color(i, max, maxColor) {
	var white = '#FFFFFF';
	if ( i > 0 ) {
		var ratio = parseInt( i ) / parseInt( max );
		var hex = function(x) {
			if ( x > 255 ) x = 255; // overflow fix...
			x = x.toString(16);
			return (x.length == 1) ? '0' + x : x;
		};

		var r = Math.ceil(parseInt(maxColor.substring(1,3), 16) * ratio + parseInt(white.substring(1,3), 16) * (1-ratio));
		var g = Math.ceil(parseInt(maxColor.substring(3,5), 16) * ratio + parseInt(white.substring(3,5), 16) * (1-ratio));
		var b = Math.ceil(parseInt(maxColor.substring(5,7), 16) * ratio + parseInt(white.substring(5,7), 16) * (1-ratio));
		resultColor = '#' + hex(r) + hex(g) + hex(b);		
	} else {
		resultColor = white;
	}
	return resultColor;
}

function hide_region_texts(	) {
	for ( var region in regions ) {
		document.getElementById( 'text_' + region ).style.display = 'none';
	}
}

function m_over_region( id ) {
	id = id.split( '_' );
	document.getElementById( 'path_' + id[1] ).style.fill = '#8BC34A';
	document.getElementById( 'cases' ).style.display = 'block';
	document.getElementById( 'cases_tspan_region' ).innerHTML = regions[ id[1] ];
	document.getElementById( 'cases_tspan_count' ).innerHTML = resultArray[ id[1] ]['value'];
}

function m_out_region( id ) {
	id = id.split('_');
	document.getElementById( 'path_' + id[1] ).style.fill = resultArray[ id[1] ]['color'];
	document.getElementById( 'cases' ).style.display = 'none';
}

function applyResults( resultArray ) {
	var found = false;
	
	
}

function changeViewTo( id ) {
	for (var key in types) {
		document.getElementById( 'selector_' + key ).style.fontWeight = "normal";
	}
	document.getElementById( id ).style.fontWeight = "bold";
	id = id.split('_');
	for (var regionKey in fullResultArray) {
		// populate result array to be able to read out the data on mouse over
		resultArray[ regionKey ] = {};
		resultArray[ regionKey ]['value'] = fullResultArray[ regionKey ][ id[1] ];
		resultArray[ regionKey ]['color'] = value_to_color( resultArray[ regionKey ]['value'], maxArray[ id[1] ], types[ id[1] ][ 'color' ] );
		// apply color to map
		document.getElementById( 'path_'+ regionKey ).style.fill = resultArray[ regionKey ]['color'];
	}
	// set legend upper limit
	document.getElementById( 'upperCount' ).innerHTML = maxArray[ id[1] ];
	document.getElementById( 'mapHeadline' ).innerHTML = types[ id[1] ][ langKey ] + ' in Thüringen';

	// init color legend
	document.getElementById('upperLimitColor').setAttribute("stop-color", value_to_color( 1, 1, types[ id[1] ][ 'color' ] ) );
}

function generateMenu() {
	del = '';
	menu = '';
	for ( var key in types ) {
		menu = menu + del + '<span id="selector_' + key +'">' + types[ key ][ langKey ] + '</span>';
		del = '&nbsp;|&nbsp;';
	}
	
	document.getElementById( 'selectorLinks' ).innerHTML = menu;
	for ( var key in types ) {
		document.getElementById( 'selector_' + key ).onclick = (function(e) { changeViewTo( e.target.id ) } );
	}
	
}

function setDataTimeTo( timestamp ) {
	var months = ['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'];
	var date = new Date( timestamp * 1000 );
	var month = months[ date.getMonth() ];
	var min = date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes(); 
	var day = date.getDate() < 10 ? '0' + date.getDate() : date.getDate(); 
	document.getElementById( 'tspan_timestamp' ).innerHTML = 'Stand: ' + day + '. ' +month + ' ' + date.getFullYear() + ', ' + date.getHours() + ':' + min + ' Uhr';
}

function getData(){
	// read text from URL location
	var request = new XMLHttpRequest();
	var lastTimeStamp = 0;
	request.open('GET', './data/cases_thuringia.dat', true);
	request.send(null);
	request.onreadystatechange = function () {
	  	if (request.readyState === 4 && request.status === 200) {
			data = request.responseText;
			lines = data.split("\n");

			lines.forEach( element => {
				if ( element.length > 0 ) {
					var arr = element.split( "," );

					// set latest timestamp and reset max value array
					if ( lastTimeStamp < parseInt( arr[0] ) ) {
						lastTimeStamp = parseInt( arr[0] );
						
						maxArray = {  
							diff :  parseInt( arr[2] ), 
							cases : parseInt( arr[3] ),  
							hosp :  parseInt( arr[4] ),  
							serv :  parseInt( arr[5] ),  
							death : parseInt( arr[6] )
						}
					}
					
					// find the correct key to the region name
					var regionKey = '';
					for (var key in regions) {
						if ( regions[ key ] == arr[1] ) regionKey = key;
					}

					// fill the result array
					fullResultArray[ regionKey ] = {
						diff :  parseInt( arr[2] ), 
						cases : parseInt( arr[3] ),  
						hosp :  parseInt( arr[4] ),  
						serv :  parseInt( arr[5] ),  
						death : parseInt( arr[6] )
					}

					// get max value for evry map
					for ( var key in types ) {
						if ( maxArray[ key ] < fullResultArray[ regionKey ][ key ] ) maxArray[ key ] = fullResultArray[ regionKey ][ key ];
					}
				}
			});
			setDataTimeTo( lastTimeStamp );
			generateMenu();
			changeViewTo( 'selector_' + Object.keys(types)[0] );
		}
	}
}

window.onload = function () {
	// hide case count legend
	document.getElementById( 'cases' ).style.display = 'none';
    var elementTypes = ['path_', 'text_'];
	for ( var region in regions ) {
		elementTypes.forEach( elementType => {
			obj = document.getElementById( elementType + region )
			obj.onmouseover = ( function(e){ m_over_region( e.target.id ) } );
			obj.onmouseout = ( function(e){ m_out_region( e.target.id ) } );
			obj.onclick = ( function(e) { js_goto( e.target.id ) } );
		});
	}

	getData();
	document.getElementById( 'thuringiaMap' ).style.display = 'block';
}