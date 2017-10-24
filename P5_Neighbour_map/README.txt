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
	-
	
README.md

## How to run the project


1.Download the project using the following link:
  ???

2.open index.html with the browser of your choice


## Project detail
 
### Server.py

	there are mainly four parts in this file:
		1.initial DB setup
		2.Google Oauth2 authentication (gconnect(),gdisconnect() are directly from
		Udacity Restaurant Menu project with minor changes to ensure them working properly)
		3.CRUD implementation using Flask and Sqlalchemy
		4.JSON endpoint implementation

### database.py

	the database file which contains three tables:
		1.user(ID,name)
		2.categories(ID,name)
		3.item((ID,name,description,price,category_ID,user_ID )
		
### DBSampleData.py

	the database file which contains two entries which will populate our database with
	data of League of Legend/Dota Items.
	
### templates/ and static/

	the HTML and CSS as well as background image files used for this project.(the background
	image file is from the Internet)

	





## Built With

LiClipse (python3)


## Versioning

https://github.com/guberland/Udacity-FSWD-Projects

## Authors

Chao Jiang

## Acknowledgments
-Udacity Forum, stackoverflow.com, developer/google.com flickr/developer
-w3resource for flickr API request (https://www.w3resource.com/API/flickr/tutorial.php)
-Sidebar referenced from https://blackrockdigital.github.io/startbootstrap-simple-sidebar/



