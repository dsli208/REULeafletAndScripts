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

<!-- jQuery Datepicker -->
<link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
<link rel="stylesheet" href="/resources/demos/style.css">
<script src="https://code.jquery.com/jquery-1.12.4.js"></script>
<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>

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

<!-- Create a div where the graph will take place -->
<p> Histogram for Intersection X </p><br />
<div id="myDiv1"></div>

<p>Date: <input type="text" id="datepicker"></p>

<div id="myDiv2"></div>

<div id='selector_menu'>
		<select id='selector'>
			<option value='none' href='/'>Select Intersection By ID</option>
			<option value='sunday' href='?day=0'>Sunday</option>
			<option value = 'monday' href='?day=1'>Monday</option>
      <option value='tuesday' href='?day=2'>Tuesday</option>
			<option value = 'wednesday' href='?day=3'>Wednesday</option>
      <option value= 'thursday' href="?day=4">Thursday</option>
			<option value = 'friday' href="?day=5">Friday</option>
      <option value= 'saturday' href="?day=6">Saturday</option>
      <option value= 'reset' href='/'>Reset</option>
		</select>
	</div>

<script>

// This script is released to the public domain and may be used, modified and
// distributed without restrictions. Attribution not necessary but appreciated.
// Source: https://weeknumber.net/how-to/javascript

// Returns the ISO week of the date.
Date.prototype.getWeek = function() {
  var date = new Date(this.getTime());
  date.setHours(0, 0, 0, 0);
  // Thursday in current week decides the year.
  date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
  // January 4 is always in week 1.
  var week1 = new Date(date.getFullYear(), 0, 4);
  // Adjust to Thursday in week 1 and count number of weeks from date to week1.
  return 1 + Math.round(((date.getTime() - week1.getTime()) / 86400000
                        - 3 + (week1.getDay() + 6) % 7) / 7);
}

// Returns the four-digit year corresponding to the ISO week of the date.
Date.prototype.getWeekYear = function() {
  var date = new Date(this.getTime());
  date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
  return date.getFullYear();
}

// Datepicker
$( function() {
    $( "#datepicker" ).datepicker();
    $( "#datepicker" ).datepicker( "setDate", "6/4/2019" );
    var currentDate = $( "#datepicker" ).datepicker( "getDate" );
    console.log(currentDate);
  } );

var glob_int;

var glob_month;
var glob_day;
//console.log(location.search.substring(1));
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

// Data for histograms (both types)
// x1 is Sunday, x7 is Saturday
var d1 = [];
var d2 = [];
var d3 = [];
var d4 = [];
var d5 = [];
var d6 = [];
var d7 = [];



for (var i = 0; i < 500; i++) {
    d1.push(Math.floor(Math.random() * 7));
    d2.push(Math.floor(Math.random() * 7));
    d3.push(Math.floor(Math.random() * 7));
    d4.push(Math.floor(Math.random() * 7));
    d5.push(Math.floor(Math.random() * 7));
    d6.push(Math.floor(Math.random() * 7));
    d7.push(Math.floor(Math.random() * 7));
}

function processTrafficData(trafficText) {
  var lines=[];
  var allTextLines = allText.split(/\r\n|\n/);
  var headers = allTextLines[0].split(',');

  for (var i = 1; i < allTextLines.length; i++) {
    var data = allTextLines[i].split(',');
    var temp_obj = {};

    if (data.length == headers.length) {
      for (var j = 0; j < headers.length; j++) {
        if (headers[j] == 'id') { // might need to adjust header strings
          temp_obj.id = parseInt(data[j]); // how to get ID to match up with a particular graph?
        }
        if (headers[j] == 'encounters') {
          temp_obj.encounters = parseInt(data[j]);
        }
        if (headers[j] == 'date') {
          temp_obj.date = new Date(data[j]);
        }
      }

      if (temp_obj.date != null) {
        var day = temp_obj.date.getDay();
        var week = temp_obj.date.getWeek();

        
      }

      // Now sort by INTERSECTION
      if (temp_obj.id != null) {

      }
    }
  }

}

var trace1 = {
  x: d1,
  type: "histogram",
  name: "Week 0"
};
var trace2 = {
  x: d2,
  type: "histogram",
  name: "Week 1"
};
var trace3 = {
  x: d3,
  type: "histogram",
  name: "Week 2"
};
var trace4 = {
  x: d4,
  type: "histogram",
  name: "Week 3"
};
var trace5 = {
  x: d5,
  type: "histogram",
  name: "Week 4"
};
var trace6 = {
  x: d6,
  type: "histogram",
  name: "Week 5"
};
var trace7 = {
  x: d7,
  type: "histogram",
  name: "Week 6"
};

var data1 = [trace1, trace2, trace3, trace4, trace5, trace6, trace7];

var x = [];
for (var i = 0; i < 500; i ++) {
    x.push(Math.floor(Math.random() * 100));
}

var trace8 = {
    x: x,
    type: 'histogram',
  };

var data2 = [trace8]; // manually push traces of intersection id when they come in

var layout1 = {barmode: "stack",
                title: {
                  text:'Fire Truck Encounters at Traffic Intersection X',
                  font: {
                    family: 'Courier New, monospace',
                    size: 24
                  },
                  xref: 'paper',
                  //x: 0.05,
                },
                xaxis: {
                  title: {
                    text: 'Day',
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
};

var layout2 = {barmode: "stack",
                title: {
                  text:'Fire Truck Encounters at Traffic Intersections on <date>',
                  font: {
                    family: 'Courier New, monospace',
                    size: 24
                  },
                  xref: 'paper',
                  //x: 0.05,
                },
                xaxis: {
                  title: {
                    text: 'Intersection ID',
                    font: {
                      family: 'Courier New, monospace',
                      size: 18,
                      color: '#7f7f7f'
                    }
                  },
                  tickwidth: 1,
                  ticklen: 1
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
};

Plotly.newPlot("myDiv1", data1, layout1, {showSendToCloud: true});
Plotly.newPlot("myDiv2", data2, layout2, {showSendToCloud: true});

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


function isEmpty(obj) {
    for(var key in obj) {
        if(obj.hasOwnProperty(key))
            return false;
    }
    return true;
}

$(document).ready(function() {
    $.ajax({
        type: "GET",
        //url: "samplecircle.csv",
        url: "filtered_avg_data2.csv",
        //url: "final.csv",
        dataType: "text",
        success: function(data) {
          processTrafficData(data);
        }
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
