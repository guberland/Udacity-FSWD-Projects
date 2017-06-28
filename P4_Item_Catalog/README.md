# P4_Item_Catalog_Project

This is the forth Undacity Full Stack Nanodegree project, this project creates
an application that provides a list of items within a variety of categories as 
well as provide a user registration and authentication system. Registered users 
will have the ability to post, edit and delete their own items.

## Prerequisites

python 3 with Flask and Sqlalchemy

## What is in the project

server.py

DBSampleData.py

database.py

client_secrets.JSON

templates/
 	-layout.html
 
 	-index.html
 
 	-create.html
 
 	-delete.html
 
 	-edit.html
 
 	-login.html
	
static/
	-bootstrap.css
	-bootstrap.min.css
	-bootstrap-theme.css
	-bootstrap-theme.min.css
	-style.css
	-Wiki-background.jpg
	
README.md

## How to run the project


1.Download the project using the following link:
  https://github.com/guberland/Udacity-FSWD-Projects/P4_Item_Catalog/

2.extract everything in the same directory.

3.use command -python server.py to run the program.

4.open the web browser and type in http://localhost:5000/category/ to view the program.



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
-Gconnect(),Gdisconnect()  (Udacity Restaurant Menu project)

-League of Legend/Dota item description 

-background image

