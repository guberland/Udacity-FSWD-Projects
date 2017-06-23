import sys
from sqlalchemy import (Column, ForeignKey, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base=declarative_base()


    
class Catagories(Base):
    
    __tablename__ = 'catagories'
    ID = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    @property
    def serialize(self):
        return{
        'ID':self.ID,
        'name':self.name,
        }

    
    
class Item(Base):
    
    __tablename__ = 'item'
    ID = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    catagory_ID = Column(Integer,ForeignKey('catagories.ID'))
    catagory = relationship(Catagories)

    @property
    def serialize(self):
        return{
        'ID':self.ID,
        'name':self.name,
        'description':self.description,
        'price':self.price,
        'catagory_ID':self.catagory_ID}



engine = create_engine('sqlite:///itemCatalog.db')

Base.metadata.create_all(engine)


