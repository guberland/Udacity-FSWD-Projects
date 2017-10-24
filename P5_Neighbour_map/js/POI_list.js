var locations = [{name: 'Iona Beach',geoLocation: {lat: 49.21658795, lng: -123.21218491}, description:"Located just north of Vancouver International Airport, Iona Beach Regional Park is a unique area of land made up of a long, narrow jetty of sand and grass along the mouth of the Fraser River."},
        {name: 'Grouse Mountain',geoLocation: {lat: 49.380166, lng: -123.080993}, description:"The Grouse Grind is Vancouver's most used trail and is renowned for its challenge in requiring physical strength and endurance in order to make it to the top."},
        {name: 'UBC',geoLocation: {lat: 49.260635, lng: -123.246002},description:"The University of British Columbia is a global centre for research and teaching, consistently ranked among the top 20 public universities in the world."},
        {name: 'Stawamus Chief',geoLocation: {lat: 49.687428, lng: -123.127642},description:'Squamish Chief is a granite dome located adjacent to the town of Squamish, British Columbia, Canada. It towers over 700 m (2,297 ft) above the waters of nearby Howe Sound. It is often claimed to be the "second largest granite monolith in the world".'},
        {name: 'Metrotown',geoLocation: {lat: 49.227239, lng: -123.000698},description:"'Metrotown is the largest mall in British Columbia, and the third largest in Canada. The mall is located adjacent to Metrotown Station on the SkyTrain rapid transit system. Three office buildings are part of the complex along Central Boulevard."},
        {name: 'Gastown',geoLocation: {lat: 49.283064, lng: -123.107471},description:"Gastown is the original settlement that became the core of the creation of Vancouver, British Columbia. Today, it's a national historic site, at the northeast end of Downtown Vancouver."},
        {name: 'Whistler',geoLocation: {lat: 50.117056, lng: -122.953491},description:"Whistler is a town north of Vancouver, British Columbia, that's home to Whistler Blackcomb, one of the largest ski resorts in North America. "},
        {name: 'Stanley Park',geoLocation: { lat:  49.31113463, lng: -123.14558029},description:"The world-famous Stanley Park is one of the major attractions for tourists when they visit Vancouver. Located next to the downtown core, Stanley Park is full of trails for walking and biking and has numerous scenic views from English Bay to the inner harbour."},
        {name: 'Joffre Lake',geoLocation: { lat:  50.36659826, lng: -122.49738693},description:"Joffre Lakes is one of BC's most beautiful hikes and is relatively easy to access compared to other alpine lakes in the region. "},
        {name: 'Steveston Village',geoLocation: { lat:  49.1249003, lng: -123.18509459},description:"Steveston village is a historic salmon canning centre at the mouth of the South Arm of the Fraser River, on the southwest tip of Lulu Island in Richmond, British Columbia. Since 1945 it has hosted an annual Steveston Salmon Festival on July 1, Canada Day."}];


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
    $("#wrapper").toggleClass("toggled");
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
          var description=locations[i].description;
          var marker = new google.maps.Marker({
            map: map,
            position: position,
            name: name,
            animation: google.maps.Animation.DROP,
            id: i,
            content:description,

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

$.getJSON(url + "&format=json&jsoncallback=?").fail(function() {
            alert('ERROR: Failed to search Flickr for related photos');
        });




 $.getJSON(url + "&format=json&jsoncallback=?", function(data){

    $.each(data.photos.photo, function(i,item){
        src = "http://farm"+ item.farm +".static.flickr.com/"+ item.server +"/"+ item.id +"_"+ item.secret +"_m.jpg";
        $("<img/>").attr("src", src).appendTo("#images");
        if ( i == 1 ) return false;
    });
});


          infowindow.marker = marker;
          infowindow.setContent('<div class="title">' + marker.name +'</div><hr>'+'<p>'+marker.content+'</p>'+'<div id="images" ></div><hr>');
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
