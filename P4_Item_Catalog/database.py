from sqlalchemy import (Column, ForeignKey, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    ID = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return{
            'ID': self.ID,
            'name': self.name
        }


class Categories(Base):

    __tablename__ = 'categories'
    ID = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return{
            'ID': self.ID,
            'name': self.name
        }


class Item(Base):

    __tablename__ = 'item'
    ID = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    category_ID = Column(Integer, ForeignKey('categories.ID'))
    category = relationship(Categories)
    user_ID = Column(Integer, ForeignKey('user.ID'))
    user = relationship(User)

    @property
    def serialize(self):
        return{
            'ID': self.ID,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category_ID': self.category_ID,
            'user_ID': self.user_ID}


engine = create_engine('sqlite:///itemCatelog.db')
Base.metadata.create_all(engine)
