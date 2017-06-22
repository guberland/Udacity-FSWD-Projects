from flask import Flask
from flask import request,redirect,url_for
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









@app.route('/')
def name():
    return "Guberland! you are the king!"




@app.route('/main/')
def showCatagory():
    catagory = session.query(Catagories).all()
    return render_template("layout.html", Catagories=catagory)

@app.route('/main/items/')
def showItem():
    item = session.query(Item).all()
    catagory = session.query(Catagories).all()
    return render_template("index.html", Catagories=catagory,Item=item)



@app.route('/main/items/create/<int:ID>',methods=['GET','POST'])    
def createItem(ID):
    itemCreated=Item(name="guberlake")
    if request.method=="POST":
        session.add(itemCreated)
        session.commit()
        return redirect(url_for('showItem',ID=ID))
    else:
        return render_template('create.html',itemcreate=itemCreated)


@app.route('/main/items/edit/<int:ID>',methods=['GET','POST'])  
def editItem(ID):
    catagory = session.query(Catagories).all()
    itemedited=session.query(Item).filter_by(ID=ID).one()
    if request.method=="POST":

        itemedited.name=request.form['name']
        itemedited.price=request.form['price']
        itemedited.description=request.form['description']
        itemedited.catagory_ID=request.form['catagory']
            
        return redirect(url_for('showItem',ID=ID))
    else:
        return render_template('edit.html',Catagories=catagory,itemedit=itemedited)



@app.route('/main/items/delete/<int:ID>',methods=['GET','POST'])    
def deleteItem(ID):
    catagory = session.query(Catagories).all()
    itemDelete=session.query(Item).filter_by(ID=ID).one()
    if request.method=="POST":
        session.delete(itemDelete)
        session.commit()
        return redirect(url_for('showItem',ID=ID))
    else:
        return render_template('delete.html',Catagories=catagory,itemdelete=itemDelete)





if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)