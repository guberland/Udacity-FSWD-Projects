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




@app.route('/server/')
def showCatagory():
    a = session.query(Catagories).all()
    b = session.query(Item).all()
    return render_template("index.html", Catagories=a,Item=b)




@app.route('/server/create/<int:ID>',methods=['GET','POST'])    
def createCatagory(ID):
    catagoryCreated=Catagories(name="guberlake")
    if request.method=="POST":
        session.add(catagoryCreated)
        session.commit()
        return redirect(url_for('showCatagory',ID=ID))
    else:
        return render_template('create.html',catagorycreate=catagoryCreated)




@app.route('/server/delete/<int:ID>',methods=['GET','POST'])    
def deleteCatagory(ID):
    catagoryDelete=session.query(Catagories).filter_by(ID=ID).one()
    if request.method=="POST":
        session.delete(catagoryDelete)
        session.commit()
        return redirect(url_for('showCatagory',ID=ID))
    else:
        return render_template('delete.html',catagorydelete=catagoryDelete)





if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)