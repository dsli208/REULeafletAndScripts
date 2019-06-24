<?php include('inc/head.inc'); ?>
<body class="front" >
<div id="page">
  <?php include('inc/masthead.inc'); ?>
  <section role="main" id="main">
    <div class="row clearfix">
      <div id="page-title">
        <!-- <h2 class="title">Home</h2> Normally the Front page title is hidden from view by moving off screen with CSS -->
      </div>
      <div class="no-sidebars" id="content">
        <div class="region region-content block-count-1 clearfix">
          <div class="block block-system">
            <div class="content block-body clearfix">
              <div class="node clearfix">
                <div class="content">
                   <div class="block-row block-row-odd block-count-2">
                    <div class="row-content clearfix">

	<h3> Heatmap </h3>
	<div id="mapid"></div>

<head>

<title>Test Map 2</title>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.5.1/dist/leaflet.css"
	integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="
crossorigin=""/>

<script src="https://unpkg.com/leaflet@1.5.1/dist/leaflet.js"
	integrity="sha512-GffPMF3RvMeYyc1LWMHtK8EbPv0iNZ8/oTtHPx9/cc2ILxQ+u905qIwdpULaqDkyBKgOaB57QTMg7ztg8Jm2Og=="
	crossorigin=""></script>

<!-- <script src="https://raw.githubusercontent.com/pa7/heatmap.js/develop/plugins/leaflet-heatmap/leaflet-heatmap.js"></script> -->
<script src="./heatmap-min.js"></script>
<script src="./heatmap.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>

<style>

#loader {
  position: absolute;
  left: 50%;
  top: 50%;
  z-index: 1;
  width: 150px;
  height: 150px;
  margin: -75px 0 0 -75px;
  border: 16px solid #f3f3f3;
  border-radius: 50%;
  border-top: 16px solid #3498db;
  width: 120px;
  height: 120px;
  -webkit-animation: spin 2s linear infinite;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.header {
  padding: 60px;
  text-align: center;
  background: #1abc9c;
  color: white;
  font-size: 30px;
  font-family: trebuchetms;
}

.header a {
  float: left;
  color: black;
  text-align: center;
  padding: 12px;
  text-decoration: none;
  font-size: 18px;
  line-height: 25px;
  border-radius: 4px;
}

.header a.logo {
  font-size: 25px;
  font-weight: bold;
}

.header a:hover {
  background-color: #ddd;
  color: black;
}

.header a.active {
  background-color: dodgerblue;
  color: white;
}

.header-right {
  float: right;
}

@media screen and (max-width: 500px) {
  .header a {
    float: none;
    display: block;
    text-align: left;
  }
  .header-right {
    float: none;
  }
}

.info {
    padding: 8px 8px;
    font: 12px/14px Arial, Helvetica, sans-serif;
    background: white;
    background: rgba(255,255,255,0.8);
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
    border-radius: 5px;
}
.info h4 {
    margin: 0 0 5px;
    color: #777;
}

.legend {
    line-height: 18px;
    color: #555;
}
.legend i {
    width: 20px;
    height: 18px;
    float: left;
    margin-right: 8px;
    opacity: 0.7;
}

#mapid { width: 1000px; height: 500px; }

</style>

</head>

<div id="loader"></div>

<script>

var circles = [];
var mapFeatures = [];
var vehicleLocationArray;

var sunday = [];
var monday = [];
var tuesday = [];
var wednesday = [];
var thursday = [];
var friday = [];
var saturday = [];

function isEmpty(obj) {
    for(var key in obj) {
        if(obj.hasOwnProperty(key))
            return false;
    }
    return true;
}

function processData(allText) {
    // For the regular heatmap data
    var lines=[];
    var allTextLines = allText.split(/\r\n|\n/);
    var headers = allTextLines[0].split(',');

    vehicleLocationArray = new Array;
    for (var i=1; i<allTextLines.length; i++) {
      var temp_obj = {};
      var data = allTextLines[i].split(',');
      if (data.length == headers.length) {
        for (var j=0; j<headers.length; j++) {
           if (headers[j] == 'lat')
               temp_obj.lat = parseFloat(data[j]);
           if (headers[j] == 'lon')
               temp_obj.lng = parseFloat(data[j]);
           if (headers[j] == 'speed') {
               temp_obj.spd = parseFloat(data[j]);
               if(temp_obj.spd<=5) {
                 temp_obj.rad = 100;
                 temp_obj.color = "#800026";
               }
               else if(temp_obj.spd <=15) {
                 temp_obj.rad = 90;
                 temp_obj.color = "#BD0026";
               }
               else if(temp_obj.spd<=25) {
                 temp_obj.rad = 80;
                 temp_obj.color = "#E31A1C";
               }
               else if(temp_obj.spd <= 35) {
                 temp_obj.rad = 70;
                 temp_obj.color = "#FC4E2A";
               }
               else if(temp_obj.spd <= 45) {
                 temp_obj.rad = 60;
                 temp_obj.color = "#FD8D3C";
               }
               else if(temp_obj.spd > 45) {
                 temp_obj.rad = 50;
                 temp_obj.color = "#FEB24C";
               }
            }
           if (headers[j] == 'time'){
               var timestamp = new Date(data[j]);
                temp_obj.hour = timestamp.getHours();
               temp_obj.day = timestamp.getDay();
           }
       }
     }
     if (!isEmpty(temp_obj)) {
       vehicleLocationArray.push(temp_obj);
     }
   }
    /*
              // Sort by day
              temp_day = day;
            }

            var temp_obj = {lat : temp_obj.lat,
            				  lng : temp_obj.lng,
            				  count : temp_count};

            var temp_feature = {
              "type": "Feature",
              "properties": {
                "name": "Data Point",
                "show_on_map": true
              },
              "geometry": {
                "type": "Point",
                "coordinates": [temp_obj.lat, temp_obj.lng]
              }
            }
            	//tarr.push(temp_obj);
            lines.push(temp_obj);
            circles.push(temp_circ);
            mapFeatures.push(temp_feature);

            console.log(lines[i-1]);
        }
    }*/

    console.log(circles);
    var smthg = [{lat: 34.022398, lng:-84.119096, count: 10}, {lat: 33.969825, lng:-84.223736, count: 5}]
	console.log("smthg "+smthg.length);

	var testData = {
	  max: 10000000,
	  data: lines
	};

	var baseLayer = L.tileLayer(
	  'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
		attribution: '...',
		maxZoom: 18
	  }
	);

	var cfg = {
	  // radius should be small ONLY if scaleRadius is true (or small radius is intended)
	  // if scaleRadius is false it will be the constant radius used in pixels
	  "radius": .001,
	  "maxOpacity": .5,
	  // scales the radius based on map zoom
	  "scaleRadius": true,
	  // if set to false the heatmap uses the global maximum for colorization
	  // if activated: uses the data maximum within the current map boundaries
	  //   (there will always be a red spot with useLocalExtremas true)
	  "useLocalExtrema": true,
	  // which field name in your data represents the latitude - default "lat"
	  latField: 'lat',
	  // which field name in your data represents the longitude - default "lng"
	  lngField: 'lng',
	  // which field name in your data represents the data value - default "value"
	  valueField: 'count'
	};

	var heatmapLayer = new HeatmapOverlay(cfg);

	var mymap = L.map('mapid', {
		center: [34.022398, -84.119096],
		zoom: 11.35,
		layers: [baseLayer, heatmapLayer]
		});

		L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
			attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery � <a href="https://www.mapbox.com/">Mapbox</a>',
			maxZoom: 18,
			id: 'mapbox.streets',
			accessToken: 'pk.eyJ1IjoiYWxhdTMzIiwiYSI6ImNqd2phYTZ4ODAzbnk0YW9lYWdzOTlpZGEifQ.4hhK6mhqi2brriiB7bEyuw'
	}).addTo(mymap);

  //L.control.layers(null, overlayMaps).addTo(mymap);

  for (var i = 0; i < vehicleLocationArray.length; i++) {
    var obj = vehicleLocationArray[i];
    console.log(obj);
    //Change the size and color of circular markers here
    circle = L.circle([obj.lat, obj.lng], {
      color: 'none',
      fillColor: obj.color,
      fillOpacity: 0.5,
      radius: obj.rad
    });
    circle.addTo(mymap);

    // Add geoJSON features
    var feature = {
      "type": "Feature",
      "properties": {
        "name": "Data Point",
        "show_on_map": true
      },
      "geometry": {
        "type": "Point",
        "coordinates": [obj.lat, obj.lng]
      }
    }

    mapFeatures.push(feature);
  }

  console.log(mapFeatures);

  var overlayMaps = {
    "Sunday": sunday,
    "Monday": monday,
    "Tuesday": tuesday,
    "Wednesday": wednesday,
    "Thursday": thursday,
    "Friday": friday,
    "Saturday": saturday
};

//L.control.layers(null, overlayMaps).addTo(mymap);

  // Info control
  var info = L.control({position: 'bottomleft'});

  info.onAdd = function (mymap) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
  };

// method that we will use to update the control based on feature properties passed
info.update = function (props) {
    this._div.innerHTML = '<h4>Fire truck speeds in Gwinnett County</h4>' +  (props ?
        '<b>' + props.lat + '</b><br />' + props.lng + ' / mi<sup>2</sup>'
        : 'Hover over a circle <br />');
};

info.addTo(mymap);

  // add interaction
  function getColor(speed) {
      return speed > 45  ? '#FEB24C' :
             speed > 35  ? '#FD8D3C' :
             speed > 25  ? '#FC4E2A' :
             speed > 15   ? '#E31A1C' :
             speed > 5   ? '#BD0026' :
             speed > 0   ? '#800026' :
                        '#FFEDA0';
  }

  function style(feature) {
  		return {
  			weight: 2,
  			opacity: 1,
  			color: 'white',
  			dashArray: '3',
  			fillOpacity: 0.7,
  			fillColor: getColor(feature.properties.density)
  		};
  	}

  	function highlightFeature(e) {
      console.log("Highlight Feature");

  		var layer = e.target;

  		layer.setStyle({
  			weight: 5,
  			color: '#666',
  			dashArray: '',
  			fillOpacity: 0.7
  		});

  		if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
  			layer.bringToFront();
  		}

  		info.update(layer.feature.properties);
  	}

  	var geojson;

  	function resetHighlight(e) {
      console.log("Reset Highlight");
  		geojson.resetStyle(e.target);
  		info.update();
  	}

  	function zoomToFeature(e) {
      console.log("Zoom to Feature");
  		map.fitBounds(e.target.getBounds());
  	}

  	function onEachFeature(feature, layer) {
      console.log("On each feature");
  		layer.on({
  			mouseover: highlightFeature,
  			mouseout: resetHighlight,
  			click: zoomToFeature
  		});
  	}

    var mapData = {"type":"FeatureCollection","features": mapFeatures};
    //console.log(mapData);
    console.log("Map features");
    console.log(mapFeatures);

  	geojson = L.geoJson(mapFeatures, {
  		style: style,
  		onEachFeature: onEachFeature
  	}).addTo(mymap);

  // new heatmap code 6/19/2019

  var legend = L.control({position: 'bottomright'});

  legend.onAdd = function (mymap) {

      var div = L.DomUtil.create('div', 'info legend'),
          grades = [0, 5, 15, 25, 35, 45],
          labels = ['Categories'];

      // loop through our density intervals and generate a label with a colored square for each interval
      div.innerHTML = '<h4>Speed (in mph)</h4>';
      for (var i = 0; i < grades.length; i++) {
          div.innerHTML +=
              '<i style="background:' + getColor(grades[i] + 1) + '"></i>' +
              grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br /><br />' : '+');
      }

      return div;
  };

  legend.addTo(mymap);

};

$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: "samplecircle.csv",
        //url: "filtered_0604ecb7003b6954_20190508.csv",
        //url: "final.csv",
        dataType: "text",
        success: function(data) {processData(data);}
     });
});

</script>

<br />
<br />

                    </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- /#content -->
    </div>
  </section>
  <!-- /#main -->

  <?php /* include('inc/superfooter.inc');  */ ?>
  <?php include('inc/footer.inc'); ?>
</div>
<!-- /#page -->

</body>
</html>
