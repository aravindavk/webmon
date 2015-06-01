// app/src/js/pebble-js-app.js
// :copyright: (c) 2015 by Aravinda VK <mail@aravindavk.in>
// :license: MIT, see LICENSE for more details.

var initialized = false;
var options = {};
var APP_URL = '<APP_URL>';

Pebble.addEventListener("ready", function() {
    console.log("ready called!");
	initialized = true;
});

Pebble.addEventListener("showConfiguration", function() {
    Pebble.openURL(
        APP_URL + '/settings?' + encodeURIComponent(JSON.stringify(options))
    );
});

Pebble.addEventListener("webviewclosed", function(e) {
    console.log("configuration closed");
    var options = JSON.parse(decodeURIComponent(e.response));
    console.log(options, options.url);
    Pebble.getTimelineToken(
        function (token) {
            console.log("Token is " + token);
            add(token, options.url, options.enabled);
        },
		function(err){
			console.log(err);
		}
	);
});

function add(user_token, url, enabled) {
    console.log("add is called");
    var xhr = new XMLHttpRequest();
    var params = "url=" + encodeURIComponent(url) +
		"&user_token=" + encodeURIComponent(user_token) +
        "&enabled=" + encodeURIComponent(enabled);

    // construct the url for the api
	var api_url = APP_URL + "/save";
	xhr.open('POST', api_url, true);
	xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhr.setRequestHeader("Content-length", params.length);     
	xhr.onload = function() {
		console.log('subscribe server response: ' + xhr.responseText);

		// Update text on the watch to say we've sent the pin
		// Pebble.sendAppMessage({text: 'Started watching ' + url, ready: true});

		// set a timer to quit the app in 2 seconds
		//setTimeout(function() {
		//Pebble.sendAppMessage({quit: true});
		//}, 2000);
	};

	xhr.send(params);
}
