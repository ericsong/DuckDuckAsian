var userID;
var beacons = new Array();        // an array of beacon objects
var courseNums = new Array();     // an array of integers

// returns response text from ajax GET command at given url
function ajaxArray(url) {
    var xmlhttp;
    if (window.XMLHttpRequest)
        {// code for IE7+, Firefox, Chrome, Opera, Safari
            xmlhttp=new XMLHttpRequest();
        }
    else
        {// code for IE6, IE5
            xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
        }
      
    xmlhttp.open("GET",url,true);
    xmlhttp.send();
      
    return xmlhttp.responseText.split("\n");
}

// returns a beacon object   -----  You will never have to use this method!
function getBeacon(beaconID) {
    var data = ajaxArray("beaconInfo.html?beaconID=" + beaconID + "&userID=" + userID);
    
    var beacon = new Object();
    beacon.courseID = data[0];
    beacon.where = data[1];
    beacon.startingTime = data[2];
    beacon.endingTime = data[3];
    beacon.notes = data[4];
    beacon.isAdmin = data[5] === "true";  // this is a boolean
    beacon.names = new Array();          // this is an array of names of users who joined the beacon
    
    for(var i = 6; i < data.length; i++) {
        names[i-6] = data[i];
    }
    
    return beacon;
}

// need to call this at beginning
function init() {
    var data = ajaxArray("initInfo.html");
    userID = data[0];
    var numberOfCourses = parseInt(data[1]);
    
    for(var i = 0; i < numberOfCourses; i++) {
        courseNums[i] = parseInt(data[2 + i]);
    }
    
    // create beacon objects
    for(var j = 2 + numberOfCourses; j < data.length; j++) {
        beacons[j - 2 - numberOfCourses] = getBeacon(data[j]);
    }
}

function courseClicked(courseNum) {
    var data = ajaxArray("beaconIDListInfo.html?courseNum=" + courseNum);
    
    // reload beacons array with new beacon objects
    beacons = new Array();
    
    for(var i = 0; i < data.length; i++) {
        beacons[0] = getBeacon(data[i]);
    }
}

function courseUnselected() {
    var data = ajaxArray("initInfo.html");
    var numberOfCourses = parseInt(data[1]);
    
    
    // reload beacons array
    beacons = new Array();
    for(var j = 2 + numberOfCourses; j < data.length; j++) {
        beacons[j - 2 - numberOfCourses] = getBeacon(data[j]);
    }
}