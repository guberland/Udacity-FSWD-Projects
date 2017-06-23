from flask import Flask, flash, jsonify
from flask import request, redirect, url_for
from flask.templating import render_template


app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Catagories, Item

engine = create_engine('sqlite:///itemCatalog.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
 
# a=Item(name="breastplate",description="tons of hp",price="4300",catagory_ID="health")
# session.add(a)
# session.commit()

@property
def serialize(self):
    return{
    'ID':self.ID,
    'name':self.name,
    'description':self.description,
    'price':self.price,
    'catagory_ID':self.catagory_ID}

@app.route('/main/catagory/all/JSON')
def showAllItemJSON():
    item = session.query(Item).all()
    return jsonify(items=[i.serialize for i in item])


@app.route('/main/catagory/JSON')
def showCatagoryJSON():
    catagory = session.query(Catagories).all()
    return jsonify(items=[i.serialize for i in catagory])


@app.route('/')
def name():
    return "Guberland! you are the king!"




@app.route('/main/catagory/')
def showCatagory():
    catagory = session.query(Catagories).all()
    return render_template("layout.html", Catagories=catagory)


@app.route('/main/catagory/all/')
def showAllItem():
    item=session.query(Item).all()
    catagory = session.query(Catagories).all()
    return render_template("index.html", Catagories=catagory,Item=item)



@app.route('/main/catagory/<name>/')
def showItem(name):
    item=session.query(Item).filter_by(catagory_ID=name).all()
    catagory = session.query(Catagories).all()
    return render_template("index.html", Catagories=catagory,Item=item)



@app.route('/main/catagory/items/create/',methods=['GET','POST'])    
def createItem():
    catagory = session.query(Catagories).all()
    if request.method=="POST":                
        itemCreated=Item(name=request.form['name'],
                     price=request.form['price'],
                     description=request.form['description'],
                     catagory_ID=request.form['catagory'])
        
        session.add(itemCreated)
        session.commit()
        flash("your item has been created!")
        return redirect(url_for('showItem',name=itemCreated.catagory_ID))
    else:
        return render_template('create.html',Catagories=catagory)


@app.route('/main/catagory/items/edit/<int:ID>',methods=['GET','POST'])  
def editItem(ID):
    catagory = session.query(Catagories).all()
    itemedited=session.query(Item).filter_by(ID=ID).one()
    if request.method=="POST":

        itemedited.name=request.form['name']
        itemedited.price=request.form['price']
        itemedited.description=request.form['description']
        itemedited.catagory_ID=request.form['catagory']
        flash("your item has been edited!")   
        return redirect(url_for('showItem',name=itemedited.catagory_ID))
    else:
        return render_template('edit.html',Catagories=catagory,itemedit=itemedited)



@app.route('/main/catagory/items/delete/<int:ID>',methods=['GET','POST'])    
def deleteItem(ID):
    catagory = session.query(Catagories).all()
    itemDelete=session.query(Item).filter_by(ID=ID).one()
    if request.method=="POST":
        session.delete(itemDelete)
        session.commit()
        flash("your item has been deleted!")   
        return redirect(url_for('showItem',name=itemDelete.catagory_ID))
    else:
        return render_template('delete.html',Catagories=catagory,itemdelete=itemDelete)





if __name__ == '__main__':
    app.secret_key='some key'
    app.run(debug = True, host = '0.0.0.0', port = 5000)