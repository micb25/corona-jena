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

var types = { diff :  'Entwicklung der Fallzahlen zum Vortag', 
    cases : 'Fallzahlen',  
    hosp :  'Stationäre Fälle',  
    serv :  'Schwere Fallverläufe',  
    death : 'Verstorbene'};

var resultArray = {};
var fullResultArray = {};
var maxArray = {};
var max = 0;
var last_region_bg_color = '';
        
function js_goto( id ) {
    id = id.split('_');
    var link = './index_th_all.html#graph_' + id[1];
    window.location.href = link;
}

function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

function value_to_color(i, max) {
    if ( i > 0 ) {
        val = parseInt( 254 - parseInt( 223.0 * parseInt( i ) / max ) );
        return "#ffff" + val.toString(16);
    } else {
        return "#ffffff";
    }
}

function hide_region_texts(    ) {
    for (var key in regions) {
            document.getElementById('text_'+ key).style.display='none';
    }
}

function m_over_region( id ) {
    last_region_bg_color = document.getElementById( id ).style.fill;
    document.getElementById( id ).style.fill = 'rgb(113, 210, 69)';
    id = id.split('_');
    document.getElementById( 'cases' ).style.display='block';
    document.getElementById( 'cases_tspan_region' ).innerHTML = regions[ id[1] ];
    document.getElementById( 'cases_tspan_count' ).innerHTML = resultArray[ regions[ id[1] ] ];
    cases_tspan_count
}

function m_out_region( id ) {
    document.getElementById( id ).style.fill = last_region_bg_color;
    id = id.split('_');
    document.getElementById( 'text_'+ id[1] ).style.display='block';
    document.getElementById( 'cases' ).style.display='none';
}

function applyResults() {
    var found = false;
    for ( var region in resultArray ) {
        //console.log( region + ':');
        found = false;
        for (var key in regions) {
            if ( region == regions[key] ) {
                found = true;
                //console.log( value_to_color( resultArray[region], max ) );
                document.getElementById('path_'+ key).style.fill = value_to_color( resultArray[region], max );
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
  applyResults();
}

window.onload = function () {
    // init correct colors
    document.getElementById('upperLimitColor').setAttribute("stop-color", value_to_color(1,1) );
    // hide case count legend
    document.getElementById( 'cases' ).style.display='none';
    for (var region in regions) {
      element = document.getElementById('path_'+ region)
      element.onmouseover = (function(ev){ m_over_region( ev.target.id ) });
      element.onmouseout = (function(ev){ m_out_region( ev.target.id ) });
    
      element.onclick = (function(ev) { js_goto( ev.target.id ) } );
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
                fullResultArray[ arr[1] ] = {  
                    diff :  parseInt( arr[2] ), 
                    cases : parseInt( arr[3] ),  
                    hosp :  parseInt( arr[4] ),  
                    serv :  parseInt( arr[5] ),  
                    death : parseInt( arr[6] )}
                if ( maxArray['diff'] < fullResultArray[ arr[1] ]['diff'] ) maxArray['diff'] = fullResultArray[ arr[1] ]['diff'];
                if ( maxArray['cases'] < fullResultArray[ arr[1] ]['cases'] ) maxArray['cases'] = fullResultArray[ arr[1] ]['cases'];
                if ( maxArray['hosp'] < fullResultArray[ arr[1] ]['hosp'] ) maxArray['hosp'] = fullResultArray[ arr[1] ]['hosp'];
                if ( maxArray['serv'] < fullResultArray[ arr[1] ]['serv'] ) maxArray['serv'] = fullResultArray[ arr[1] ]['serv'];
                if ( maxArray['death'] < fullResultArray[ arr[1] ]['death'] ) maxArray['death'] = fullResultArray[ arr[1] ]['death'];
              }
            });
            changeViewTo('cases');
          }
      }
    }
    getText();
}