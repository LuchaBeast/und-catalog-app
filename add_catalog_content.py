from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Populate Action Figures category
category1 = Category(category_name="Action Figures")

session.add(category1)
session.commit()

item1 = Item(item_name="Masters of the Universe Vintage Skeletor", item_description="By the Power of Grayskull! Super7 is proud to present the MOTU Vintage Collection, the original Masters of the Universe action figures re-imagined to match the character designs from the animated cartoon! The Skeletor 5.5-inch Vintage Figure comes with Havoc Staff, Power Sword, and Half-Sword and features a spring loaded mechanism: Turn the waist and he swings back with a punch! The packaging includes a custom character history card with the figure and has new and original art on the back of each card by classic MOTU artist Errol McCarthy.", category=category1)

session.add(item1)
session.commit()

print("added menu items!")