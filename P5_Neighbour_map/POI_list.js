// var locations = [{name: 'place1',type:1},{name: 'place2',type:1},{name: 'place3',type:2},{name: 'place4',type:2}];
// var locationdd = ['place1','place2'];


var POIlists = function(){
    this.POIList = ko.observableArray(locations);
}


var ViewModel = function(){
    // this.currentPOIList = ko.observable(new POIlists());

    this.locations = ko.observableArray([{name: 'place1',type:'one'},
        {name: 'place2',type:'one'},{name: 'place3',type:'two'},
        {name: 'place4',type:'two'}]);

    this.typeToShow = ko.observable("all");
    this.locationToshow = ko.computed(function() {

        var filteredType = this.typeToShow();
        if (filteredType=="all") return this.locations();
        return ko.utils.arrayFilter(this.locations(),function(location){
            return location.type == filteredType;
        });
    }, this);


}


ko.applyBindings( new ViewModel());



