# P5_Neighbourhood Map

This is the fifth Undacity Full Stack Nanodegree project, this project creates
an single web application features some of my favourite places in Vancouver that 
appears as markers on Google Map API with pictures from Flickr.

## Prerequisites

Knockout Js,Jquery,Bootstrap

## What is in the project

index.html

css/
 	-bootstrap.min.css
 
 	-style.css
 
js/
	-app.js
	-bootstrap.bundle.min.js
	-jquery-3.2.1.min.js
	-knockout-3.4.2.js
	
	
README.md

## How to run the project


1.Download the project using the following link:
  ???

2.open index.html with the browser of your choice

3.click menu to see the location list

4.click either markers on the map or location list to view the
  information and recent 2 pictures from flickr of the specified location
  
## API
 
### Google Map API

	The Google Map API is used here to generate the map and markers as well as th corresponding Info Windows,
the location list used is currently hardcoded into the App.js file as locations[]
	
### Flickr

	Each markers will send ajax request to flickr then retrieve and display 2 (or the value of i in populateInfoWindow)
recent photos of the corresponding marker	


## Built With

SubLime (HTML,CSS,JS)


## Versioning

https://github.com/guberland/Udacity-FSWD-Projects

## Authors

Chao Jiang

## Acknowledgments
-Udacity and its Forum, stackoverflow.com, developer/google.com flickr/developer
-w3resource for flickr API request (https://www.w3resource.com/API/flickr/tutorial.php)
-Sidebar referenced from https://blackrockdigital.github.io/startbootstrap-simple-sidebar/



