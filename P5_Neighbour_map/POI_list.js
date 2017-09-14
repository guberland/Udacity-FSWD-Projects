var locations = [{name: 'Iona Beach',type:'one',geoLocation: {lat: 49.21658795, lng: -123.21218491},visb:'yes'},
        {name: 'Stanley Park',type:'one',geoLocation: { lat:  49.31113463, lng: -123.14558029},visb:'yes'},
        {name: 'Joffre Lake',type:'two',geoLocation: { lat:  50.36659826, lng: -122.49738693},visb:'yes'},
        {name: 'Steveston Village',type:'two',geoLocation: { lat:  49.1249003, lng: -123.18509459},visb:'yes'}];
// var locationdd = ['place1','place2'];

var map;
var markers=[];

 var initMap = function() {
        map = new google.maps.Map(document.getElementById('map'), {
          center: {lat:  33.126, lng: -117.311},
          zoom: 8
        });

        this.renderMarker();

}

var ViewModel = function(){
    // this.currentPOIList = ko.observable(new POIlists());
    var self = this;
    self.locations = ko.observableArray(locations);
    self.typeToShow = ko.observable("all");


    self.locationToshow = ko.computed(function() {

        var filteredType = this.typeToShow();
        if (filteredType=="all") return this.locations();
        return ko.utils.arrayFilter(this.locations(),function(location){
            return location.type == filteredType;
        });
    }, self);



}

function centerMarker(){google.maps.event.trigger(self.marker, 'click');}






function deleteMarker(){
       for(i=0; i<markers.length; i++){
        markers[i].setMap(null);
    }

}

function renderMarker(){

    var largeInfowindow = new google.maps.InfoWindow();



     var bounds = new google.maps.LatLngBounds();
        this.deleteMarker();
        for (var i = 0; i < locations.length; i++) {




          var position = locations[i].geoLocation;
          var name = locations[i].name;

          var marker = new google.maps.Marker({
            map: map,
            position: position,
            name: name,
            animation: google.maps.Animation.DROP,
            id: i

          });


          markers.push(marker);

          bounds.extend(markers[i].position);

          map.fitBounds(bounds);

          marker.addListener('click', function() {
            populateInfoWindow(this, largeInfowindow);
            var currentCenter = this.getPosition();
            map.setCenter(currentCenter);
            map.setZoom(12);
          });

  }

   // function centerMarker()
   // {
   //  map.setCenter(this.geoLocation);
   //  map.setZoom(12);
   //  populateInfoWindow(this, largeInfowindow);
   //  }


function populateInfoWindow(marker, infowindow) {

        // Check to make sure the infowindow is not already opened on this marker.
        if (infowindow.marker != marker) {
          infowindow.marker = marker;
          infowindow.setContent('<div>' + marker.name +'</div>');
          infowindow.open(map, marker);
          // Make sure the marker property is cleared if the infowindow is closed.
          infowindow.addListener('closeclick',function(){
            infowindow.setMarker = null;
          });
      }
    }
}




ko.applyBindings( new ViewModel());
