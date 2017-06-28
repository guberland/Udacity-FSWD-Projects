from flask import Flask, flash, jsonify
from flask import request, redirect, url_for
from flask.templating import render_template
import DBSampleData


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Categories, Item, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catelog Application"

engine = create_engine('sqlite:///itemCatelog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def addCatagory(category):
    """two helper functions that extract data from DBSampleData.py"""
    """and fill the corresponding tables"""
    for i in category:
        categories = Categories(name=i)
        session.add(categories)
        session.commit


def addItem(item):
    for i in item:
        items = Item(name=i[0], price=i[1], description=i[2],
                     category_ID=i[3], user_ID=i[4])
        session.add(items)
        session.commit

    """If the table is empty, create dummy user and execute the helper"""
    """functions to populate the tables"""
if session.query(Categories.ID).all() == []:
    session.rollback()
    dummyUser = User(name="guberland")
    session.add(dummyUser)
    session.commit
    addCatagory(DBSampleData.SampleCategory)
    addItem(DBSampleData.SampleItem)
# Create anti-forgery state token


@app.route('/login/')
def showLogin():
    """create anti 32 bit forgery token and bring the user to login page"""
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Google Oauth2 connection implementation"""
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    a = h.request(url, 'GET')[1]
    result = json.loads(a.decode('utf-8'))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user '
                                 'is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    a = session.query(User).all()
    if not session.query(User).filter_by(name=login_session['email']).all():
        flash("Welcome!")
        newUser = User(name=login_session['email'])
        session.add(newUser)
        session.commit()
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += """ " style = "width: 300px; height: 300px;border-radius:
    150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> """
    flash("you are now logged in as %s" % login_session['username'])
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """Google Oauth2 disconnection implementation"""
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user '
                                            'not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/'
    'revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token'
                                            'for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/main/category/all/JSON')
def showAllItemJSON():
    """show JSON of all items stored"""
    item = session.query(Item).all()
    return jsonify(items=[i.serialize for i in item])


@app.route('/main/category/JSON')
def showCategoryJSON():
    """show JSON of all categories created"""
    category = session.query(Categories).all()
    return jsonify(Categories=[i.serialize for i in category])


@app.route('/main/category/')
def showCategory():
    """the template file which all other HTMLs extends from"""
    category = session.query(Categories).all()
    return render_template("layout.html", Categories=category)


@app.route('/main/category/all/')
def showAllItem():
    """show items stored"""
    item = session.query(Item).all()
    category = session.query(Categories).all()
    return render_template("index.html", Categories=category, Item=item)


@app.route('/main/category/<name>/')
def showItem(name):
    """show items in the corresponding category"""
    item = session.query(Item).filter_by(category_ID=name).all()
    category = session.query(Categories).all()
    return render_template("index.html", Categories=category, Item=item)


@app.route('/main/category/myitem/')
def userItem():
    """show current user's item list"""
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(Item).filter_by(user_ID=login_session['email']).all()
    category = session.query(Categories).all()
    return render_template("index.html", Categories=category, Item=item)


@app.route('/main/category/items/create/', methods=['GET', 'POST'])
def createItem():
    """takes user to the create item page if user is logged in,otherwise"""
    """redirect to the login page"""
    category = session.query(Categories).all()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == "POST":
        itemCreated = Item(name=request.form['name'],
                           price = request.form['price'],
                           description = request.form['description'],
                           category_ID=request.form['category'],
                           user_ID = login_session['email'])

        session.add(itemCreated)
        session.commit()
        flash("your item has been created!")
        return redirect(url_for('showItem', name=itemCreated.category_ID))
    else:
        return render_template('create.html', Categories=category)


@app.route('/main/category/items/edit/<int:ID>', methods=['GET', 'POST'])
def editItem(ID):
    """takes user to the edit item page if user is logged in,otherwise"""
    """redirect to the login page"""
    category = session.query(Categories).all()
    itemedited = session.query(Item).filter_by(ID=ID).one()

    if 'username' not in login_session:
        return redirect('/login')
    current_user = login_session['email']

    if login_session['email'] != itemedited.user_ID:
        flash("Sorry,only the owner of the item can edit this item")
        return redirect(url_for('showItem', name=itemedited.category_ID))

    if request.method == "POST":
        itemedited.name = request.form['name']
        itemedited.price = request.form['price']
        itemedited.description = request.form['description']
        itemedited.category_ID = request.form['category']
        flash("your item has been edited!")
        return redirect(url_for('showItem', name=itemedited.category_ID))
    else:
        return render_template('edit.html', Categories=category,
                               itemedit=itemedited, current_user=current_user)


@app.route('/main/category/items/delete/<int:ID>', methods=['GET', 'POST'])
def deleteItem(ID):
    """takes user to the delete item page if user is logged in,otherwise"""
    """redirect to the login page"""
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Categories).all()
    itemDelete = session.query(Item).filter_by(ID=ID).one()
    if login_session['email'] != itemDelete.user_ID:
        flash("Sorry,only the owner of the item can delete this item")
        return redirect(url_for('showItem', name=itemDelete.category_ID))
    if request.method == "POST":
        session.delete(itemDelete)
        session.commit()
        flash("your item has been deleted!")
        return redirect(url_for('showItem', name=itemDelete.category_ID))
    else:
        return render_template('delete.html', Categories=category,
                               itemdelete=itemDelete)


if __name__ == '__main__':
    app.secret_key = 'some key'
    app.run(debug = True, host = '0.0.0.0', port = 5000)
