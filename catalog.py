from flask import Flask
from flask import render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/c/<int:category_id>/<string:category_name>/')
def category_page(category_id, category_name):
    all_categories = session.query(Category).all()
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(Item).filter_by(category_id = category_id)
    return render_template('category.html', all_categories = all_categories, category = category, items = items)

@app.route('/category/item/')
def item_page():
    return render_template('item.html')
    
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)