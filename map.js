// basic region infos
// { region_key : { name: 'xxx', res: 12, area: 34 } }
// src:
// - residents: https://statistik.thueringen.de/datenbank/TabAnzeige.asp?tabelle=gg000102&startpage=99&vorspalte=1&felder=2&zeit=2018%7C%7Cs1
// - area: https://statistik.thueringen.de/datenbank/TabAnzeige.asp?tabelle=GG000101%7C%7C
var regions = {
	ABG: { name: "Altenburger Land", res: 90118, area: 569.40 },
	EIC: { name: "Eichsfeld", res: 100380, area: 943.07 },
	EA:  { name: "Eisenach", res: 42370, area: 104.17 },
	EF:  { name: "Erfurt", res: 213699, area: 269.91 },
	G:   { name: "Gera", res: 94152, area: 152.18 },
	GTH: { name: "Gotha", res: 135452, area: 936.08 },
	GRZ: { name: "Greiz", res: 98159, area: 845.98 },
	HBN: { name: "Hildburghausen", res: 63553, area: 938.42 },
	IK:  { name: "Ilm-Kreis", res: 108742, area: 843.71 },
	J:   { name: "Jena", res: 111407, area: 114.77 },
	KYF: { name: "Kyffhäuserkreis", res: 75009, area: 1037.91 },
	NDH: { name: "Nordhausen", res: 83822, area: 713.90 },
	SHK: { name: "Saale-Holzland-Kreis", res: 83051, area: 815.24 },
	SOK: { name: "Saale-Orla-Kreis", res: 80868, area: 1151.30 },
	SLF: { name: "Saalfeld-Rudolstadt", res: 106356, area: 1036.03 },
	SM:  { name: "Schmalkalden-Meiningen", res: 122347, area: 1210.73 },
	SOM: { name: "Sömmerda", res: 69655, area: 806.86 },
	SON: { name: "Sonneberg", res: 56196, area: 433.61 },
	SHL: { name: "Suhl", res: 34835, area: 103.03 },
	UH:  { name: "Unstrut-Hainich-Kreis", res: 102912, area: 979.69 },
	WAK: { name: "Wartburgkreis", res: 123025, area: 1307.44 },
	WE:  { name: "Weimar", res: 65090, area: 84.48 },
	AP:  { name: "Weimarer Land", res: 81947, area: 804.48 }
};

// map types and colors
// { var_key : { de: 'xxx', en: 'xxx', color: '#000000' } }
var types = {
	cases : {
		de: 'Fallzahlen',
		color: '#0000D3',
		unit : 'Fälle' },
	diff : {
		de: 'Entwicklung der Fallzahlen',
		color: '#A000FF',
		unit : 'Fälle / Tag',
		pm : 1 },
	hosp : {
		de: 'Stationäre Fälle',
		color: '#FFAD00',
		unit : 'Fälle' },
	serv : {
		de: 'Schwere Fallverläufe',
		color: '#D30000',
		unit : 'Fälle' },
	death : {
		de: 'Verstorbene', 
		color: '#333333',
		unit : 'Fälle' }
};

var resultArray = {};
var fullResultArray = {};
var maxArray = {};
var langKey = 'de';
var actualType = '';
		
function js_goto( id ) {
	id = id.split('_');

	document.getElementById( 'graphBlockContainer' ).style.display='block';
	document.getElementById( 'graph_variable' ).src='https://www.michael-böhme.de/corona/plotT1_' + id[1] + '.png';
	document.getElementById( 'graph_headline' ).innerHTML = regions[ id[1] ]['name'];
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
	hsp = Math.sqrt(
		0.299 * (bgColorRGB['r'] ** 2) +
		0.587 * (bgColorRGB['g'] ** 2) +
		0.114 * (bgColorRGB['b'] ** 2)
		);

	var resultColor = '#000000';
	if ( hsp < 0.6*255 ) {
		resultColor = '#FFFFFF';
	}
	return resultColor;
}

function hide_region_texts(	) {
	for ( var region in regions ) {
		document.getElementById( 'text_' + region ).style.display = 'none';
	}
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

	return result.toString().replace(".",",");
}

function m_over_region( id ) {
	id = id.split( '_' );
	document.getElementById( 'path_' + id[1] ).style.fill = '#8BC34A';
	document.getElementById( 'cases' ).style.display = 'block';
	document.getElementById( 'cases_tspan_region' ).innerHTML = regions[ id[1] ]['name'];
	
	var value = formatValue( resultArray[ id[1] ]['value'] );
	console.log( actualType );
	if ( 'pm' in types[ actualType ] ) {
		if ( types[ actualType ][ 'pm' ] == 1 ) {
			prefix = ( resultArray[ id[1] ]['value'] >= 0 ) ? '+ ' : '- ';
			value = prefix  + value; 
		}
	}
	if ( 'unit' in types[ actualType ] ) {
		value = value + ' ' + types[ actualType ][ 'unit' ];
	}
	document.getElementById( 'cases_tspan_count' ).innerHTML = value;
}

function m_out_region( id ) {
	id = id.split('_');
	document.getElementById( 'path_' + id[1] ).style.fill = resultArray[ id[1] ]['color'];
	document.getElementById( 'cases' ).style.display = 'none';
}

function changeViewTo( id ) {
	for (var key in types) {
		document.getElementById( 'selector_' + key ).style.fontWeight = "normal";
	}
	document.getElementById( id ).style.fontWeight = "bold";
	actualType = id.split('_')[1];

	for (var regionKey in fullResultArray) {
		// populate result array to be able to read out the data on mouse over
		resultArray[ regionKey ] = {};
		resultArray[ regionKey ]['value'] = fullResultArray[ regionKey ][ actualType ];
		resultArray[ regionKey ]['color'] = valueToColor( resultArray[ regionKey ]['value'], maxArray[ actualType ], types[ actualType ][ 'color' ] );
		// apply color to map
		document.getElementById( 'path_'+ regionKey ).style.fill = resultArray[ regionKey ]['color'];
		document.getElementById( 'text_'+ regionKey ).style.fill = getOverlayTextColor( resultArray[ regionKey ]['color'] );
		
	}
	// set legend upper limit
	value = formatValue( maxArray[ actualType ] );
	if ( 'pm' in types[ actualType ] ) {
		if ( types[ actualType ][ 'pm' ] == 1 ) {
			prefix = ( maxArray[ actualType ] >= 0 ) ? '+ ' : '- ';
			value = prefix  + value; 
		}
	}
	document.getElementById( 'upperCount' ).innerHTML = value;
	document.getElementById( 'mapHeadline' ).innerHTML = types[ actualType ][ langKey ] + ' in Thüringen';
	document.getElementById( 'cases_text_headline' ).innerHTML = types[ actualType ][ langKey ]; 

	// init color legend
	document.getElementById('upperLimitColor').setAttribute("stop-color", valueToColor( 1, 1, types[ actualType ][ 'color' ] ) );
}

function generateMenu() {
	del = '';
	menu = '';
	cnt = 0;
	maxItemsPerLine = 5;
	for ( var key in types ) {
		cnt++;
		menu = menu + del + '<span id="selector_' + key +'">' + types[ key ][ langKey ] + '</span>';
		if ( cnt % maxItemsPerLine ) {
			del = '&nbsp;|&nbsp;';
		} else{
			del = '<br>';
		}
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

function getMaxValues() {
	for (var regionKey in regions) {
		for ( var type in types ) {
			if ( maxArray[ type ] < fullResultArray[ regionKey ][ type ] ) maxArray[ type ] = fullResultArray[ regionKey ][ type ];
		}
	}
}

function getProcessedData() {
	var processedTypes = {
		casedens : {
			de: 'Flächenbezogene Fälle',
			color: '#0000D3',
			unit : 'Fälle / km²' },
		caseres : {
			de: 'relative Fallzahlen',
			color: '#0000D3',
			unit : 'Fälle / 100.000 EW' },
		area : {
			de: 'Fläche',
			color: '#00A000',
			unit : 'km²' },
		res : {
			de: 'Einwohner',
			color: '#00A000',
			unit : 'EW' },
		dens : {
			de: 'Einwohnerdichte',
			color: '#00A000',
			unit : 'EW / km²' },
	};

	for (var regionKey in regions) {
		// fill the result array
		fullResultArray[ regionKey ]['area']		= regions[regionKey]['area'];
		fullResultArray[ regionKey ]['res']			= regions[regionKey]['res'];
		fullResultArray[ regionKey ]['dens']		= regions[regionKey]['res'] / regions[ regionKey ][ 'area' ];
		fullResultArray[ regionKey ]['casedens']	= fullResultArray[ regionKey ][ 'cases' ] / regions[ regionKey ][ 'area' ];
		fullResultArray[ regionKey ]['caseres']		= fullResultArray[ regionKey ][ 'cases' ] / regions[ regionKey ][ 'res' ]*100000;
	}
	
	for ( var type in processedTypes ) {
		types[ type ] = processedTypes[ type ];
		maxArray[ type ] = 0;
	}
}

function getData() {
	// read text from URL location
	var request = new XMLHttpRequest();
	var lastTimeStamp = 0;
	request.open('GET', './data/cases_thuringia.csv', true);
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
					
					// find the correct regionKey to the region name
					var regionKey = '';
					for (var key in regions) {
						if ( regions[ key ]['name'] == arr[1] ) {
							regionKey = key;
						}
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
					for ( var type in types ) {
						if ( maxArray[ type ] < fullResultArray[ regionKey ][ type ] ) maxArray[ type ] = fullResultArray[ regionKey ][ type ];
					}
				}
			});
			getProcessedData();
			getMaxValues();
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
