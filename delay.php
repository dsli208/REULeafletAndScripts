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


<head>

<title>Test Map 2</title>
<!-- Add Leaflet.js heat map sources -->
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

<!-- include cartodb css  -->
<link rel="stylesheet" href="http://libs.cartocdn.com/cartodb.js/v3/3.15/themes/css/cartodb.css" />
<!-- include cartodb.js library -->
<script src="http://libs.cartocdn.com/cartodb.js/v3/3.15/cartodb.js"></script>

<!-- Load d3.js/plotly.js -->
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
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

/* Dropdown Button */
.dropbtn {
  background-color: #3498DB;
  color: white;
  padding: 16px;
  font-size: 16px;
  border: none;
  cursor: pointer;
}

/* Dropdown button on hover & focus */
.dropbtn:hover, .dropbtn:focus {
  background-color: #2980B9;
}

/* The container <div> - needed to position the dropdown content */
.dropdown {
  position: relative;
  display: inline-block;
}

/* Dropdown Content (Hidden by Default) */
.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f1f1f1;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

/* Links inside the dropdown */
.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

/* Change color of dropdown links on hover */
.dropdown-content a:hover {background-color: #ddd}

/* Show the dropdown menu (use JS to add this class to the .dropdown-content container when the user clicks on the dropdown button) */
.show {display:block;}

/*New, INSIDE Leaflet map drop down*/
html, body,
      #selector_menu{
      	position: bottomright;
      	top: 20px;
      	left: 20px;
      	z-index: 9000;
      }

#mapid { width: 1200px; height: 800px; }

</style>

</head>

<div id="loader"></div>

<h3> Delay Map </h3>
<!--
<div class="dropdown">
  <button onclick="showDropDown()" class="dropbtn">Select Day</button><br />
  <div id="myDropdown" class="dropdown-content">
    <a href="/">Reset</a>
    <a href="?day=0">Sunday</a>
    <a href="?day=1">Monday</a>
    <a href="?day=2">Tuesday</a>
    <a href="?day=3">Wednesday</a>
    <a href="?day=4">Thursday</a>
    <a href="?day=5">Friday</a>
    <a href="?day=6">Saturday</a>
  </div>
</div>

-->
<br />
<div id="mapid"></div>

<!-- Create a div where the graph will take place -->
<!--<p> Histogram for Intersection X </p><br /> -->
<div id="myDiv"></div>

<!--
<div id='selector_menu'>
		<select id='selector'>
			<option value='none' href='/'>Select Day</option>
			<option value='sunday' href='?day=0'>Sunday</option>
			<option value = 'monday' href='?day=1'>Monday</option>
      <option value='tuesday' href='?day=2'>Tuesday</option>
			<option value = 'wednesday' href='?day=3'>Wednesday</option>
      <option value='thursday' href="?day=4">Thursday</option>
			<option value = 'friday' href="?day=5">Friday</option>
      <option value='saturday' href="?day=6">Saturday</option>
      <option value='reset' href='/'>Reset</option>
		</select>
	</div>
-->

<script>

/*var x1 = [];
var x2 = [];
var x3 = [];
var x4 = [];
var x5 = [];
var x6 = [];
var x7 = [];

for (var i = 0; i < 500; i++) {
    x1[i] = Math.floor(Math.random() * 7);
    x2[i] = Math.floor(Math.random() * 7);
    x3[i] = Math.floor(Math.random() * 7);
    x4[i] = Math.floor(Math.random() * 7);
    x5[i] = Math.floor(Math.random() * 7);
    x6[i] = Math.floor(Math.random() * 7);
    x7[i] = Math.floor(Math.random() * 7);
}

var trace1 = {
  x: x1,
  type: "histogram",
  name: "Week 0"
};
var trace2 = {
  x: x2,
  type: "histogram",
  name: "Week 1"
};
var trace3 = {
  x: x3,
  type: "histogram",
  name: "Week 2"
};
var trace4 = {
  x: x4,
  type: "histogram",
  name: "Week 3"
};
var trace5 = {
  x: x5,
  type: "histogram",
  name: "Week 4"
};
var trace6 = {
  x: x6,
  type: "histogram",
  name: "Week 5"
};
var trace7 = {
  x: x7,
  type: "histogram",
  name: "Week 6"
};

var data1 = [trace1, trace2, trace3, trace4, trace5, trace6, trace7];
//console.log(data);
var layout1 = {barmode: "stack",
                title: {
                  text:'Fire Truck Encounters at Traffic Intersection X',
                  font: {
                    family: 'Courier New, monospace',
                    size: 24
                    //align: 'center'
                  },
                  xref: 'paper',
                  //x: 0.05,
                },
                xaxis: {
                  title: {
                    text: 'Day of Week',
                    font: {
                      family: 'Courier New, monospace',
                      size: 18,
                      color: '#7f7f7f'
                    }
                  },
                },
                yaxis: {
                  title: {
                    text: 'Intersection Encounters',
                    font: {
                      family: 'Courier New, monospace',
                      size: 18,
                      color: '#7f7f7f'
                    }
                  }}
};*/

//Plotly.newPlot("myDiv", data1, layout1, {showSendToCloud: true});

// Code that could be used for filtering by day
var glob_day;
console.log(location.search.substring(1));
if (location.search.substring(1) == 'day=0') {
  glob_day = 0;
}
else if (location.search.substring(1) == 'day=1') {
  glob_day = 1;
}
else if (location.search.substring(1) == 'day=2') {
  glob_day = 2;
}
else if (location.search.substring(1) == 'day=3') {
  glob_day = 3;
}
else if (location.search.substring(1) == 'day=4') {
  glob_day = 4;
}
else if (location.search.substring(1) == 'day=5') {
  glob_day = 5;
}
else if (location.search.substring(1) == 'day=6') {
  glob_day = 6;
}
else {
  glob_day = -1;
}

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function showDropDown() {
  document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

// Array for circle objects to be displayed on map
var circles = [];
var mapFeatures = [];
var vehicleLocationArray;

// Arrays for potentially filtering by day...
var sunday = [];
var monday = [];
var tuesday = [];
var wednesday = [];
var thursday = [];
var friday = [];
var saturday = [];
// .. as well as time of day too
var morning = [];
var midday = [];
var afternoon = [];
var evening = [];
var night = [];
var dawn = [];

// Is an array object empty
function isEmpty(obj) {
    for(var key in obj) {
        if(obj.hasOwnProperty(key))
            return false;
    }
    return true;
}

// Like speed map (index.php), this function reads in data and adds it to the Leaflet bubble map
function processData(allText) {
    // For the regular heatmap data
    var lines=[];
    var allTextLines = allText.split(/\r\n|\n/);
    var headers = allTextLines[0].split(',');

    // Array with objects detailing (emergency) vehicle locations
    vehicleLocationArray = new Array;
    for (var i=1; i<allTextLines.length; i++) {
      var temp_obj = {};
      var data = allTextLines[i].split(',');
      if (data.length == headers.length) {
        // Identifying category by header, then setting object value to correspond with associated data
        for (var j=0; j<headers.length; j++) {
           if (headers[j] == 'CenterLatitude')
               temp_obj.lat = parseFloat(data[j]);
           if (headers[j] == 'CenterLongitude')
               temp_obj.lng = parseFloat(data[j]);
           if (headers[j] == 'Average Delays(sec)') {
               temp_obj.delay = parseFloat(data[j]);
               if(temp_obj.delay <= 10 || temp_obj.delay == null) {
                 temp_obj.rad = 150;
                 temp_obj.color = "#808080";

               }
               else if(temp_obj.delay <= 20) {
                 temp_obj.rad = 150;
                 temp_obj.color = "#1A8508";
               }
               else if(temp_obj.delay<= 30) {
                 temp_obj.rad = 150;
                 temp_obj.color = "#99D923";
               }
               else if(temp_obj.delay <= 40) {
                 temp_obj.rad = 150;
                 temp_obj.color = "#FFFB00";

               }
               else if(temp_obj.delay <= 50) {
                 temp_obj.rad = 150;
                 temp_obj.color = "#FFAA00";

               }
               else if(temp_obj.delay > 50) {
                 temp_obj.rad = 150;
                 temp_obj.color = "#800026";
                 //temp_obj.color = "#28C90C";
               }
            }
           if (headers[j] == 'time'){
               var timestamp = new Date(data[j]);
               console.log(timestamp);
               console.log(timestamp.getTimezoneOffset());
               temp_obj.hour = timestamp.getHours();
               temp_obj.day = timestamp.getDay();
           }
       }
     }
     // Ensure object isn't empty and is valid before adding it to vehicle locations
     if (!isEmpty(temp_obj) && (temp_obj.day == glob_day || glob_day < 0)) {
       vehicleLocationArray.push(temp_obj);
     }
   }

    console.log(circles);
    var smthg = [{lat: 34.022398, lng:-84.119096, count: 10}, {lat: 33.969825, lng:-84.223736, count: 5}]
	console.log("smthg "+smthg.length);

	var testData = {
	  max: 10000000,
	  data: lines
	};

  // Getting map sources and attributes
  var oldMapURL = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    oldMapAttr = '...';
  var mbAttr = 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
			'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		mbUrl = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';

  // Base layer of map
	var baseLayer   = L.tileLayer(mbUrl, {id: 'mapbox.light', attribution: mbAttr});

	var baseLayer1 = L.tileLayer(
	  mbUrl,{
      id: 'mapbox.light',
		attribution: mbAttr,
		maxZoom: 30
	  }
	);

  // Basework for heat map layer
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

  // Configure Leaflet map
	var mymap = L.map('mapid', {
		center: [33.965759, -84.096407],
		zoom: 12,
		layers: [baseLayer, heatmapLayer]
		});

		/*L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
			attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery � <a href="https://www.mapbox.com/">Mapbox</a>',
			maxZoom: 18,
			id: 'mapbox.streets',
			accessToken: 'pk.eyJ1IjoiYWxhdTMzIiwiYSI6ImNqd2phYTZ4ODAzbnk0YW9lYWdzOTlpZGEifQ.4hhK6mhqi2brriiB7bEyuw'
	}).addTo(mymap);*/

  // Adding each of the locations onto the map
  for (var i = 0; i < vehicleLocationArray.length; i++) {
    var obj = vehicleLocationArray[i];
    console.log(obj);
    //Change the size and color of circular markers here
    circle = L.circle([obj.lat, obj.lng], {
      color: 'none',
      fillColor: obj.color,
      fillOpacity: 0.8,
      radius: obj.rad
    });
    circle.addTo(mymap);
    circles.push(circle);

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

    // Future code for potentially filtering by day
      if (obj.day == 0) {
        console.log("Sunday");
        sunday.push(circle);
      }
      else if (obj.day == 1) {
        console.log("Monday");
        monday.push(circle);
      }
      else if (obj.day == 2) {
        console.log("Tuesday");
        tuesday.push(circle);
      }
      else if (obj.day == 3) {
        console.log("Wednesday");
        wednesday.push(circle);
      }
      else if (obj.day == 4) {
        console.log("Thursday");
        thursday.push(circle);
      }
      else if (obj.day == 5) {
        console.log("Friday");
        friday.push(circle);
      }
      else if (obj.day == 6) {
        console.log("Saturday");
        saturday.push(circle);
      }


        if (obj.hour >= 3 && obj.hour < 7) {
          console.log("Dawn");
          dawn.push(circle);
        }
        else if (obj.hour >= 7 && obj.hour < 11) {
          console.log("Morning");
          morning.push(circle);
        }
        else if (obj.hour >= 11 && obj.hour < 15) {
          console.log("Midday");
          midday.push(circle);
        }
        else if (obj.hour >= 15 && obj.hour < 19) {
          console.log("Afternoon");
          afternoon.push(circle);
        }
        else if (obj.hour >= 19 && obj.hour < 23) {
          console.log("Evening");
          evening.push(circle);
        }
        else if (obj.hour >= 23 || obj.hour <3) {
          console.log("Night");
          night.push(circle);
        }
  }

  // Add functionality for each point in the map (mouseover and click)
  console.log(circles);
  circles.forEach(function(obj) {
        var index = circles.indexOf(obj);
        console.log(index);
				//obj[0].bindPopup('ID: '+obj[1].site_id);
				obj.on('mouseover', function (e) {
					//this.openPopup();
					info.update(vehicleLocationArray[index]);
				});
				obj.on('mouseout', function (e) {
					//this.closePopup();
					info.update();
			  });
        obj.on('click', function(e) {
          zoomToFeature(e);
        })
	});

  console.log(mapData);

  // Convert arrays to layergroups
  var sundayLayer = L.layerGroup(sunday).addTo(mymap);
  var mondayLayer = L.layerGroup(monday).addTo(mymap);
  var tuesdayLayer = L.layerGroup(tuesday).addTo(mymap);
  var wednesdayLayer = L.layerGroup(wednesday).addTo(mymap);
  var thursdayLayer = L.layerGroup(thursday).addTo(mymap);
  var fridayLayer = L.layerGroup(friday).addTo(mymap);
  var saturdayLayer = L.layerGroup(saturday).addTo(mymap);

  // Time of day layers
  var dawnLayer = L.layerGroup(dawn).addTo(mymap);
  var morningLayer = L.layerGroup(morning).addTo(mymap);
  var middayLayer = L.layerGroup(midday).addTo(mymap);
  var afternoonLayer = L.layerGroup(afternoon).addTo(mymap);
  var eveningLayer = L.layerGroup(evening).addTo(mymap);
  var nightLayer = L.layerGroup(night).addTo(mymap);

  console.log("Sunday layer");
  console.log(sunday); console.log(sundayLayer);

  var overlayMaps = {
    "Sunday": sundayLayer,
    "Monday": mondayLayer,
    "Tuesday": tuesdayLayer,
    "Wednesday": wednesdayLayer,
    "Thursday": thursdayLayer,
    "Friday": fridayLayer,
    "Saturday": saturdayLayer,
    "Dawn": dawnLayer,
    "Morning": morningLayer,
    "Midday": middayLayer,
    "Afternoon": afternoonLayer,
    "Evening": eveningLayer,
    "Night": nightLayer
  };

  L.control.layers(null, overlayMaps).addTo(mymap);

  // Info control
  var info = L.control({position: 'bottomleft'});

  info.onAdd = function (mymap) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
  };

// method that we will use to update the control based on feature properties passed
info.update = function (props) {
    this._div.innerHTML = '<h4>Fire Truck Delays in Gwinnett County</h4>' +  (props ?
        '' + props.lat + ', ' + props.lng + '<br /><b>'+ props.delay + ' sec </b>'
        : 'Hover over an intersection <br />');
};

info.addTo(mymap);

  // add interaction
  function getColor(d) {
    return d > 50  ? '#800026' :
           d > 40  ?  '#FFAA00' :
           d > 30  ?  '#FFFB00' :
           d > 20   ? '#99D923' :
           d > 10   ? '#1A8508' :
           d > 0   ?  '#808080' :
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
  		mymap.fitBounds(e.target.getBounds());
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

  // Code for map legend, see index.php for more details
  var legend = L.control({position: 'bottomright'});

  legend.onAdd = function (mymap) {

      var div = L.DomUtil.create('div', 'info legend'),
          grades = [0, 10, 20, 30, 40, 50],
          labels = ['Categories'];

      // loop through our density intervals and generate a label with a colored square for each interval
      div.innerHTML = '<h4>Delay (seconds)</h4>';
      for (var i = 0; i < grades.length; i++) {
          div.innerHTML +=
              '<i style="background:' + getColor(grades[i] + 1) + '"></i>' +
              grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br /><br />' : '+');
      }

      return div;
  };

  legend.addTo(mymap);

};

// Placeholder code for selector, could be used to filter by day
$('#selector').change(function() {
		console.log($(this).val());
    var day = $(this).val();

    if (day == 'sunday') {
      window.location.replace("?day=0");
    }
    else if (day == 'monday') {
      window.location.replace("?day=1");
    }
    else if (day == 'tuesday') {
      window.location.replace("?day=2");
    }
    else if (day == 'wednesday') {
      window.location.replace("?day=3");
    }
    else if (day == 'thursday') {
      window.location.replace("?day=4");
    }
    else if (day == 'friday') {
      window.location.replace("?day=5");
    }
    else if (day == 'saturday') {
      window.location.replace("?day=6");
    }
    else {
      window.location.replace("/");
    }
});

// AJAX code for reading in data file
$(document).ready(function() {
    $.ajax({
        type: "GET",
        //url: "samplecircle.csv",
        url: "IntersectionAverages.csv",
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
