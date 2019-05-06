import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# Create category table
class Category(Base):
    __tablename__ = 'category'
    category_name = Column(String, nullable = False)
    id = Column(Integer, primary_key = True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'category_name': self.category_name,
        }

# Create item table
class Item(Base):
    __tablename__ = 'item'
    item_name = Column(String, nullable = False)
    id = Column(Integer, primary_key = True)
    item_description = Column(String)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'item_name': self.item_name,
            'item_description': self.item_description,
        }
        

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)