//Declaring global variables
var map;
var markers = [];


initMap = function() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: {
            lat: 33.126,
            lng: -117.311
        },
        zoom: 8
    });
    this.renderMarker();
};


var ViewModel = function() {
    var self = this;
    this.locations = ko.observableArray(locations);
    this.typeToShow = ko.observable("all");
    this.filteredMarker = ko.observableArray([]);
    this.query = ko.observable("");
    this.name = ko.observable("");

    //search function to match the item with text input and hide/show corresponding markers
    this.search = function(value) {
        self.locations([]);
        for (var x in locations) {
            if (locations[x].name.toLowerCase().indexOf(value.toLowerCase()) >= 0) {
                self.locations.push(locations[x]);
                markers[x].setVisible(true);
            }
            else markers[x].setVisible(false);
        }
    };

    this.query.subscribe(self.search);

    //list click function that triggers click request on the corresponding marker
    this.centerMarker = function() {
        var index = 0;
        var markerName = this.name;
        $("#wrapper").toggleClass("toggled");

        for (var x in markers) {
            if (markers[x].name == markerName) {
                index = x;
                break;
            }
            else index = -1;
        }

        google.maps.event.trigger(markers[index], "click");
    };
};


function renderMarker() {
    var largeInfowindow = new google.maps.InfoWindow();
    var bounds = new google.maps.LatLngBounds();

    for (var i = 0; i < locations.length; i++) {
        var position = locations[i].geoLocation;
        var name = locations[i].name;
        var type = locations[i].type;
        var description = locations[i].description;

        var marker = new google.maps.Marker({
            map: map,
            position: position,
            name: name,
            animation: google.maps.Animation.DROP,
            id: i,
            content: description,
        });

        markers.push(marker);
        bounds.extend(markers[i].position);
        map.fitBounds(bounds);

        marker.addListener("click", clickMarker);
    }

    google.maps.event.addDomListener(window, "resize", function() {
        map.fitBounds(bounds);
    });

    //zoom and center the map to the clicked marker with a popping animation
    function clickMarker() {
        console.log(marker);
        this.setAnimation(4);
        var currentInfoWindow = null;
        var currentCenter = this.getPosition();
        populateInfoWindow(this, largeInfowindow);
        map.setCenter(currentCenter);
        map.setZoom(12);
    }

    function populateInfoWindow(marker, infowindow) {
        var currentInfoWindow = infowindow;
        if (infowindow.marker != marker) {
            infowindow.marker = marker;
            var infoContent = '<div class="title">' + marker.name + "</div><hr>" + "<p>" + marker.content + "</p>" + "<hr>";
            infowindow.setContent(infoContent);
            infowindow.open(map, marker);
            var src = "";
            var url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=de5e8d74b7c261bce18d9b92acff771d&tags=" + marker.name;
            //function that does ajax request from flickr to fill the Info Window with i(2) pictures
            $.getJSON(url + "&format=json&jsoncallback=?", function(data) {
                $.each(data.photos.photo, function(i, item) {
                    src += "<img src = \"http://farm" + item.farm + ".static.flickr.com/" + item.server + "/" + item.id + "_" + item.secret + "_m.jpg\">";
                    infoContent = '<div class="title">' + marker.name + "</div><hr>" + "<p>" + marker.content + "</p>" + src + "<hr>";
                    infowindow.setContent(infoContent);
                    console.log(src);
                    if (i == 1) return false;
                });
                //Ajax call error handling
            }).fail(function() {
                alert("ERROR: Failed to search Flickr for related photos");
            });


            infowindow.addListener("closeclick", function() {
                infowindow.setMarker = null;
            });
        }
    }
}
function googleError(){
    window.alert("failed to load Google Map");
}
//Knockout Binding
var viewModel = new ViewModel();
ko.applyBindings(viewModel);