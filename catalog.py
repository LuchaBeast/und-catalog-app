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
    all_categories = session.query(Category).all()
    all_items = session.query(Item).all()
    return render_template('index.html', all_categories = all_categories, all_items = all_items)

@app.route('/c/<int:category_id>/<string:category_name>/')
def category_page(category_id, category_name):
    all_categories = session.query(Category).all()
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(Item).filter_by(category_id = category_id)
    return render_template('category.html', all_categories = all_categories, category = category, items = items)

@app.route('/c/<int:category_id>/<string:category_name>/<int:id>/<string:item_name>/')
def item_page(category_id, category_name, id, item_name):
    all_categories = session.query(Category).all()
    category = session.query(Category).filter_by(id = category_id).one()
    item = session.query(Item).filter_by(category_id = category_id).filter_by(id = id).one()
    return render_template('item.html', all_categories = all_categories, category = category, item = item)
    
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)