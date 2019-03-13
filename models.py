from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, index=True)
    google_sub = Column(String, nullable = False)

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key = True)
    category_name = Column(String(32),nullable = False)

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer,primary_key = True)
    item_name = Column(String(32), nullable = False)
    item_description = Column(String(300))  
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User')


engine = create_engine('sqlite:///item_category_app.db', connect_args={'check_same_thread': False})
 

Base.metadata.create_all(engine)

