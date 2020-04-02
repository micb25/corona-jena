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

var types = { diff :  'Entwicklung der Fallzahlen', 
	cases : 'Fallzahlen',  
	hosp :  'Stationäre Fälle',  
	serv :  'Schwere Fallverläufe',  
	death : 'Verstorbene'};
	
var colorByType = { diff :  '#A000FFFF', 
	cases : '#0000d3',  
	hosp :  '#FFAD00',  
	serv :  '#D30000',  
	death : '#333333'};

var resultArray = {};
var fullResultArray = {};
var maxArray = {};
var max = 0;
var last_region_bg_color = '';
var color = '';
		
function js_goto( id ) {
	id = id.split('_');

	document.getElementById( 'graphBlockContainer' ).style.display='block';
	document.getElementById( 'graph_variable' ).src='./plotT1_' + id[1] + '.png';
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
		
		//console.log(i + '/' +max + ': h' +hex(r) + ', d' + r);
		
	} else {
		resultColor = white;
	}
	//console.log( resultColor );
	return resultColor;
}

function hide_region_texts(	) {
	for (var key in regions) {
			document.getElementById('text_'+ key).style.display='none';
	}
}

function m_over_region( id ) {
	id = id.split('_');
	last_region_bg_color = document.getElementById( 'path_' + id[1] ).style.fill;
	document.getElementById( 'path_' + id[1] ).style.fill = 'rgb(113, 210, 69)';
	document.getElementById( 'cases' ).style.display='block';
	document.getElementById( 'cases_tspan_region' ).innerHTML = regions[ id[1] ];
	document.getElementById( 'cases_tspan_count' ).innerHTML = resultArray[ regions[ id[1] ] ];
}

function m_out_region( id ) {
	id = id.split('_');
	document.getElementById( 'path_' + id[1] ).style.fill = last_region_bg_color;
	document.getElementById( 'cases' ).style.display='none';
}

function applyResults() {
	var found = false;
	
	// init color legend
	document.getElementById('upperLimitColor').setAttribute("stop-color", value_to_color(1,1, color) );
	
	for ( var region in resultArray ) {
		//console.log( region + ':');
		found = false;
		for (var key in regions) {
			if ( region == regions[key] ) {
				found = true;
				document.getElementById('path_'+ key).style.fill = value_to_color( resultArray[region], max, color );
			}
		}
		if ( found == false ) {
			console.log(region + ' not found');
		}
	}
}

function changeViewTo( id ) {
  for (var region in fullResultArray) {
	resultArray[ region ] = fullResultArray[ region ][ id ];
	max = maxArray[ id ];
  }
  // set legend upper limit
  document.getElementById('upperCount').innerHTML = max;
  document.getElementById( 'mapHeadline' ).innerHTML = types[ id ] + ' in Thüringen';
  color = colorByType[ id ];
  applyResults();
}

function getText(){
	// read text from URL location
	var request = new XMLHttpRequest();
	var lastTimeStamp = 0;
	request.open('GET', './data/cases_thuringia.dat', true);
	request.send(null);
	request.onreadystatechange = function () {
	  if (request.readyState === 4 && request.status === 200) {
		data = request.responseText;
		lines = data.split("\n");

		lines.forEach(element => {
		  if ( element.length > 0 ) {
			var arr = element.split( "," );

			if ( lastTimeStamp < parseInt( arr[0] ) ) {
			  lastTimeStamp = parseInt( arr[0] );
			  maxArray = {  
				diff :  parseInt( arr[2] ), 
				cases : parseInt( arr[3] ),  
				hosp :  parseInt( arr[4] ),  
				serv :  parseInt( arr[5] ),  
				death : parseInt( arr[6] )}
			}
			var months = ['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'];
			var date = new Date(lastTimeStamp * 1000);
			var month = months[date.getMonth()];
			var min = date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes(); 
			var day = date.getDate() < 10 ? '0' + date.getDate() : date.getDate(); 
			document.getElementById( 'tspan_timestamp' ).innerHTML = 'Stand: ' + day + '.' +month + ' ' + date.getFullYear() + ', ' + date.getHours() + ':' + min + ' Uhr';
			
			fullResultArray[ arr[1] ] = {  
				diff :  parseInt( arr[2] ), 
				cases : parseInt( arr[3] ),  
				hosp :  parseInt( arr[4] ),  
				serv :  parseInt( arr[5] ),  
				death : parseInt( arr[6] )}
			for (var type in types) {
				if ( maxArray[ type ] < fullResultArray[ arr[1] ][ type ] ) maxArray[ type ] = fullResultArray[ arr[1] ][ type ];
			}
		  }
		});
		changeViewTo('cases');
	  }
	}
	
}
window.onload = function () {
	// hide case count legend
	document.getElementById( 'cases' ).style.display='none';
	for (var region in regions) {
	  element = document.getElementById('path_'+ region)
	  element.onmouseover = (function(ev){ m_over_region( ev.target.id ) });
	  element.onmouseout = (function(ev){ m_out_region( ev.target.id ) });
	  element.onclick = (function(ev) { js_goto( ev.target.id ) } );

	  element = document.getElementById('text_'+ region)
	  element.onmouseover = (function(ev){ m_over_region( ev.target.id ) });
	  element.onmouseout = (function(ev){ m_out_region( ev.target.id ) });
	  element.onclick = (function(ev) { js_goto( ev.target.id ) } );
	}

	getText();
	document.getElementById( 'thuringiaMap' ).style.display='block';
}