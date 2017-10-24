var locations = [{name: 'Iona Beach',type:'one',geoLocation: {lat: 49.21658795, lng: -123.21218491},visb:'true'},
        {name: 'Stanley Park',type:'one',geoLocation: { lat:  49.31113463, lng: -123.14558029},visb:'true'},
        {name: 'Joffre Lake',type:'two',geoLocation: { lat:  50.36659826, lng: -122.49738693},visb:'true'},
        {name: 'Steveston Village',type:'two',geoLocation: { lat:  49.1249003, lng: -123.18509459},visb:'true'}];
// var locationdd = ['place1','place2'];

var map;
var markers=[];

     initMap = function() {
        map = new google.maps.Map(document.getElementById('map'), {
          center: {lat:  33.126, lng: -117.311},
          zoom: 8
        });

        this.renderMarker();


}



var ViewModel = function(){

    var self = this;
    this.locations = ko.observableArray(locations);
    this.typeToShow = ko.observable("all");
    this.filteredMarker=ko.observableArray([]);
    this.query=ko.observable('');
    this.name=ko.observable("");
    this.search = function(value) {

     self.locations([]);

    for(var x in locations) {
      if(locations[x].name.toLowerCase().indexOf(value.toLowerCase()) >= 0) {
        self.locations.push(locations[x]);
              markers[x].setVisible(true);
            }
            else markers[x].setVisible(false);
    }
  }
  this.query.subscribe(self.search);










  this.centerMarker=function(){
    var index=0;
    var markerName=this.name;
;
    for (var x in markers){

      if (markers[x].name==markerName)
         {index=x;
          break;}

      else index=-1;
    }


  google.maps.event.trigger(markers[index], 'click');
}

};
    // self.locationToshow = ko.computed(function() {

    //     var filteredType = this.typeToShow();

    //     if (filteredType=="all") return this.locations();
    //     return ko.utils.arrayFilter(this.locations(),function(location){
    //         return location.type == filteredType;
    //     });
    // }, self);











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
          var type = locations[i].type;
          var marker = new google.maps.Marker({
            map: map,
            position: position,
            name: name,
            animation: google.maps.Animation.DROP,
            id: i

            // type: type;
          });
          // ViewModel.locations()[i].marker = marker;

          markers.push(marker);

          bounds.extend(markers[i].position);

          map.fitBounds(bounds);

          marker.addListener('click', function() {
          // this.setIcon('http://maps.google.com/mapfiles/ms/icons/green-dot.png');
          this.setAnimation(4);





            var currentInfoWindow=null;
            populateInfoWindow(this, largeInfowindow);
            var currentCenter = this.getPosition();
            map.setCenter(currentCenter);
            map.setZoom(12);
          });

  }




function populateInfoWindow(marker, infowindow) {










        var currentInfoWindow=infowindow;
        // Check to make sure the infowindow is not already opened on this marker.
        if (infowindow.marker != marker) {

var url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=de5e8d74b7c261bce18d9b92acff771d&tags="+marker.name;
var src;
$.getJSON(url + "&format=json&jsoncallback=?", function(data){
    $.each(data.photos.photo, function(i,item){
        src = "http://farm"+ item.farm +".static.flickr.com/"+ item.server +"/"+ item.id +"_"+ item.secret +"_m.jpg";
        $("<img/>").attr("src", src).appendTo("#images");
        if ( i == 1 ) return false;
    });
});
    console.log(src);
          infowindow.marker = marker;
          infowindow.setContent('<div>' + marker.name +'</div>'+'<div id="images"></div>');
          infowindow.open(map, marker);
          // Make sure the marker property is cleared if the infowindow is closed.
          infowindow.addListener('closeclick',function(){
            infowindow.setMarker = null;
          });
      }
    }
}



var viewModel = new ViewModel();
ko.applyBindings(viewModel);
