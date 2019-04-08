import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
    category_name = Column(String, nullable = False)
    id = Column(Integer, primary_key = True)

class Item(Base):
    __tablename__ = 'item'

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)